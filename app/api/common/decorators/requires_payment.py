from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from api.common.services.mongodb import get_db


def requires_payment(f):
    db = get_db()
    """Decorator function to prevent non-subscripted users to access features."""

    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()

        # Fetch the user from the database using the user
        current_user = db.users.find_one(current_user)

        if current_user is None or not current_user["active_subscription"]:
            return jsonify({"error": "User has not an active subscription"}), 401

        return f(*args, **kwargs)

    return decorated
