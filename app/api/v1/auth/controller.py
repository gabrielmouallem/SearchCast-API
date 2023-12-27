import datetime
from flask import jsonify
import re
from passlib.hash import pbkdf2_sha256
import uuid
from flask_jwt_extended import create_access_token
import requests
from api.v1.auth.dto import GoogleLoginDTO, GoogleResponseDTO, PasswordLoginDTO, UserDTO
from api.common.decorators.requires_auth import get_db


class UserController:
    def __init__(self) -> None:
        self.db = get_db()

    def start_session(self, user: UserDTO):
        if "password" in user:
            del user["password"]
        # Concatenate user data and generate a hash as the access token
        access_token = create_access_token(identity=user)
        return jsonify({**user, "access_token": access_token}), 200

    def register_w_password(self, register: UserDTO):
        # Validate name
        name = register.name
        if name is None or len(name) < 3:
            return jsonify({"error": "Invalid name"}), 400

        # Validate email
        email = register.email
        if not self._is_valid_email(email):
            return jsonify({"error": "Invalid email address"}), 400

        # Validate password
        password = register.password
        if not self._is_valid_password(password):
            return jsonify({"error": "Invalid password"}), 400

        id = uuid.uuid4().hex

        # Create the user object
        user = {
            "_id": id,
            "name": name,
            "email": email,
            "password": password,
            "active_subscription": False,
            "auth_type": "password",
            "created_on": datetime.datetime.utcnow().isoformat(),
        }

        # Encrypt the password
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        # Check for existing email address
        if self.db.users.find_one({"email": user["email"]}):
            return jsonify({"error": "Email address already in use"}), 400

        if self.db.users.insert_one(user):
            user_without_password = {**user}
            del user_without_password["password"]
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def start_session_w_google(self, register: GoogleLoginDTO):
        print("start_session_w_google")
        id = uuid.uuid4().hex

        # Create the user object
        user = {
            "_id": id,
            "name": register.name,
            "email": register.email,
            "active_subscription": False,
            "auth_type": "google",
            "created_on": datetime.datetime.utcnow().isoformat(),
        }

        # Check for existing email address
        to_find_user = self.db.users.find_one(
            {"email": user["email"]}
        )  # To get proper active_subscription value
        if to_find_user:
            return self.start_session(to_find_user)

        if self.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def _is_valid_email(self, email):
        email_regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        return re.match(email_regex, email)

    def _is_valid_password(self, password):
        # Password should have at least 8 characters, including at least one digit and one special symbol
        return (
            len(password) >= 8
            and any(c.isdigit() for c in password)
            and any(c.isalnum() for c in password)
        )

    def password_login(self, login: PasswordLoginDTO):
        db = get_db()
        user = db.users.find_one({"email": login.email})

        if user and pbkdf2_sha256.verify(login.password, user["password"]):
            user_without_password = {**user}
            del user_without_password["password"]
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401

    def google_login(self, login: GoogleLoginDTO):
        google_response = login.google_response
        # Verify Google Access Token
        google_token = google_response.id_token
        if not google_token:
            return jsonify({"error": "Invalid Google Sign-In response"}), 400

        google_user_info = self.verify_google_token(google_token)
        if not google_user_info:
            return jsonify({"error": "Google token verification failed"}), 401

        print(self.start_session_w_google(register=login))
        return self.start_session_w_google(register=login)

    def verify_google_token(self, google_token):
        # Verify the Google access token using Google's API
        google_response = requests.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={google_token}"
        )
        if google_response.status_code == 200:
            return google_response.json()
        return None
