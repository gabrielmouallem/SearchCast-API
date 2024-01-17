from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from api.common.services.mongodb import get_db
import time


def requires_payment(f):
    db = get_db()

    def decorated(*args, **kwargs):
        verify_jwt_in_request()
        current_user = get_jwt_identity()

        # Fetch the user from the database using the user ID
        user_data = db.users.find_one({"email": current_user["email"]})

        # Check if allow_unpaid_access is True
        if user_data.get("allow_unpaid_access", False):
            return f(*args, **kwargs)

        # Check if subscription status is incomplete and current_period_end is expired
        subscription = user_data.get("subscription", {})
        current_period_end = subscription.get("current_period_end", 0)
        current_date = int(time.time())

        if current_period_end < current_date:
            return (
                jsonify(
                    {"message": "Payment required", "error": "Subscription expired"}
                ),
                403,
            )

        return f(*args, **kwargs)

    return decorated
