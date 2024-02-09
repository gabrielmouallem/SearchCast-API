import datetime
import os
import time
from flask import jsonify
import re
from passlib.hash import pbkdf2_sha256
import uuid
from flask_jwt_extended import create_access_token
import requests
from api.v1.auth.dto import GoogleLoginDTO, PasswordLoginDTO, UserDTO
from api.common.decorators.requires_auth import get_db
from api.common.utils.utils import get_proper_user_data
from api.common.services.email.email_service import EmailService

EXPIRATION_TIME = 30 * 60

flask_env = os.environ.get("FLASK_ENV")

FRONTEND_URL = f"{os.environ.get("FRONTEND_URL")}/password-reset"


def generate_reset_password_email(token):
    html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Redefinição de Senha - SearchCast</title>
        <style>
        .container {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }}
        .email-content {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .btn {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #009EA4;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
        }}
        .btn:hover {{
            background-color: #007d80;
        }}
        </style>
        </head>
        <body>
        <div class="container">
        <div class="email-content">
            <h2>Redefinição de Senha - SearchCast</h2>
            <p>Olá,</p>
            <p>Você está recebendo este e-mail porque solicitou a redefinição de senha para sua conta no SearchCast. Para redefinir sua senha, clique no botão abaixo:</p>
            <div>
            <a href="{FRONTEND_URL}?token={token}" class="btn" style="color: white; text-decoration: none;">Redefinir Senha</a>
            </div>
            <p>Se você não solicitou essa redefinição, pode ignorar este e-mail.</p>
            <p>Obrigado,<br>Equipe SearchCast</p>
        </div>
        </div>
        </body>
        </html>
    """
    return html_content


class UserController:
    def __init__(self) -> None:
        self.db = get_db()

    def start_session(self, user: UserDTO):
        if "password" in user:
            del user["password"]
        # Concatenate user data and generate a hash as the access token
        user_data = get_proper_user_data(user)
        access_token = create_access_token(identity=user_data)
        return jsonify({**user_data, "access_token": access_token}), 200

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
            "allow_unpaid_access": False,
            "password": password,
            "auth_type": "password",
            "created_on": datetime.datetime.utcnow().isoformat(),
        }

        # Encrypt the password
        user["password"] = pbkdf2_sha256.encrypt(user["password"])

        # Check for existing email address
        if self.db.users.find_one({"email": user["email"]}):
            return jsonify({"error": "Email address already in use"}), 400

        if self.db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def start_session_w_google(self, register: GoogleLoginDTO):
        id = uuid.uuid4().hex

        # Create the user object
        user = {
            "_id": id,
            "name": register.name,
            "email": register.email,
            "allow_unpaid_access": False,
            "auth_type": "google",
            "created_on": datetime.datetime.utcnow().isoformat(),
        }

        # Check for existing email address
        to_find_user = self.db.users.find_one(
            {"email": user["email"]}
        )  # To get proper user with all the user values
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
        # Verify Google Access Token
        google_token = login.id_token
        if not google_token:
            return jsonify({"error": "Invalid Google Sign-In response"}), 400

        google_user_info = self.verify_google_token(google_token)
        if not google_user_info:
            return jsonify({"error": "Google token verification failed"}), 401

        return self.start_session_w_google(register=login)

    def verify_google_token(self, google_token):
        # Verify the Google access token using Google's API
        google_response = requests.get(
            f"https://www.googleapis.com/oauth2/v3/tokeninfo?id_token={google_token}"
        )
        if google_response.status_code == 200:
            return google_response.json()
        return None

    def password_reset(self, token, new_password):

        if not self._is_valid_password(new_password):
            return jsonify({"error": "Invalid password"}), 400

        if token is None:
            print(f"{token} - password reset attempt with null email")
            return jsonify({"error": "please provide an email"}), 400

        db = get_db()
        password_reset = db.passwordResets.find_one({"token": token})

        if password_reset is None:
            print(f"Password reset attempt with no reset data on the database")
            return (
                jsonify(
                    {
                        "error": "password reset attempt with no reset data on the database"
                    }
                ),
                404,
            )

        user = db.users.find_one({"email": password_reset["email"]})

        if user is None:
            return jsonify({"error": "user not found"}), 404

        if password_reset["expiring_date"] <= int(time.time()):
            print(
                f"{user['email']} - password reset attempt while the reset is expired"
            )
            return jsonify({"error": "password reset is expired"}), 400

        if password_reset["expiring_date"] > int(time.time()):
            print(f"{user['email']} - password reset attempt is valid")
            token = uuid.uuid4().hex

            db.passwordResets.delete_one(password_reset)

            db.users.update_one(
                {"email": user["email"]},
                {
                    "$set": {
                        "password": pbkdf2_sha256.encrypt(new_password),
                    }
                },  # current time plus 30 minutes
            )
            return jsonify(success=True)

    def forgot_password(self, email):
        if email is None:
            print(f"{email} - forgot password flow attempt with null email")
            return jsonify({"error": "please provide an valid email"}), 400

        db = get_db()
        user = db.users.find_one({"email": email})

        if user is None:
            print(
                f"{email} - forgot password flow attempt with no user on the database"
            )
            return jsonify({"error": "please provide an valid email"}), 400

        password_reset = db.passwordResets.find_one({"email": email})

        if password_reset is None:
            if user["auth_type"] == "google":
                return (
                    jsonify(
                        {"error": "this account does not have password (google auth)"}
                    ),
                    400,
                )
            print(f"{email} - forgot password flow attempt first time")
            token = uuid.uuid4().hex
            expiring_date = int(time.time()) + EXPIRATION_TIME

            db.passwordResets.insert_one(
                {
                    "email": email,
                    "token": token,
                    "expiring_date": expiring_date,  # current time plus 30 minutes
                }
            )

            EmailService().send(
                {
                    "to": email,
                    "subject": "Redefinição De Senha",
                    "html": generate_reset_password_email(token),
                }
            )
            return jsonify(success=True)

        if password_reset["expiring_date"] > int(time.time()):
            print(
                f"{email} - forgot password flow attempt while another reset is not expired yet"
            )
            return jsonify(success=True)

        if password_reset["expiring_date"] <= int(time.time()):
            print(
                f"{email} - forgot password flow attempt while previous reset was expired"
            )
            token = uuid.uuid4().hex
            expiring_date = int(time.time()) + EXPIRATION_TIME

            db.passwordResets.update_one(
                {"email": email},
                {
                    "$set": {
                        "token": token,
                        "expiring_date": expiring_date,
                    }
                },  # current time plus 30 minutes
            )

            EmailService.send(
                {
                    "to": email,
                    "subject": "Redefinição De Senha",
                    "html": generate_reset_password_email(token),
                }
            )
            print(
                f"{email} - forgot password flow email sent and reset data expiring date updated"
            )

            return jsonify(success=True)
