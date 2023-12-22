from flask import jsonify, request
from api.common.services.mongodb import get_db


def check_payment(access_token):
    user = get_db().users.find_one({"access_token": access_token})
    user_has_active_payment = user is not None and user["active_subscription"]
    # Check if the user exists and has an active subscription
    print(f"check_payment: {user_has_active_payment}")
    return user_has_active_payment


def requires_payment(f):
    """Decorator function to protect routes with authentication."""

    def decorated(*args, **kwargs):
        access_token = request.headers.get("Bearer")
        if not access_token or not check_payment(access_token):
            return jsonify({"error": "Unauthorized: user hasn't subscription"}), 401
        return f(*args, **kwargs)

    return decorated
