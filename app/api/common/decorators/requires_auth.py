from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from api.common.services.mongodb import get_db


def requires_auth(f):
    db = get_db()
    """Decorator function to protect routes with JWT authentication."""

    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()

        # Fetch the user from the database using the user
        current_user = db.users.find_one(current_user)

        if current_user is None:
            return jsonify({"error": "User not found"}), 401

        return f(*args, **kwargs)

    return decorated
