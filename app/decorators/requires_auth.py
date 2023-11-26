import os
from flask import jsonify, request

SECRET_KEY = os.environ.get("SECRET_KEY")


def authenticate(api_key):
    """Function to authenticate users based on the provided API key."""
    return api_key == SECRET_KEY


def requires_auth(f):
    """Decorator function to protect routes with authentication."""

    def decorated(*args, **kwargs):
        api_key = request.headers.get("Api-Key")
        if not api_key or not authenticate(api_key):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated
