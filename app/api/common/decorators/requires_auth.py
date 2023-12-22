from flask import jsonify, request
from api.common.services.mongodb import get_db


def authenticate(access_token):
    db = get_db()
    user = db.users.find_one({"access_token": access_token})
    return user is not None


def requires_auth(f):
    """Decorator function to protect routes with authentication."""

    def decorated(*args, **kwargs):
        access_token = request.headers.get("Bearer")
        if not access_token or not authenticate(access_token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)

    return decorated
