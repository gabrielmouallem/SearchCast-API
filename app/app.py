from datetime import timedelta
import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import setup
from routes import configure_routes

env = setup()

app = Flask(__name__)
app.config.from_object(f"config.{env}.{env.capitalize()}Config")

app.secret_key = os.environ.get("SECRET_KEY")

app.config["JWT_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
    hours=24
)  # Set token expiration to 24 hours

jwt = JWTManager(app)

CORS(app)
configure_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
