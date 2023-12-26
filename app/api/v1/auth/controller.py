import datetime
from flask import jsonify, session
import re
from passlib.hash import pbkdf2_sha256
import uuid
from flask_jwt_extended import create_access_token
from api.v1.auth.dto import LoginDTO, UserDTO
from api.common.decorators.requires_auth import get_db


class UserController:
    def __init__(self) -> None:
        self.db = get_db()

    def start_session(self, user: UserDTO):
        del user["password"]
        session["logged_in"] = True
        session["user"] = user

        # Concatenate user data and generate a hash as the access token
        access_token = create_access_token(identity=user)
        session["access_token"] = access_token

        return jsonify(user), 200

    def register(self, register: UserDTO):
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
            access_token = create_access_token(identity=user_without_password)
            return self.start_session(
                {
                    **user,
                    "access_token": access_token,
                }
            )

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

    def login(self, login: LoginDTO):
        db = get_db()
        user = db.users.find_one({"email": login.email})

        if user and pbkdf2_sha256.verify(login.password, user["password"]):
            user_without_password = {**user}
            del user_without_password["password"]
            access_token = create_access_token(identity=user_without_password)
            return self.start_session(
                {
                    **user,
                    "access_token": access_token,
                }
            )

        return jsonify({"error": "Invalid login credentials"}), 401
