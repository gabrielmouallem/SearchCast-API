# routes.py
import os
from flask import Response, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
)
from api.common.decorators import requires_auth, requires_payment
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController
from api.v1.auth.controller import UserController
from api.v1.auth.dto import GoogleLoginDTO, PasswordLoginDTO, UserDTO
from api.v1.webhook.constants import (
    DEV_STRIPE_PLANS_LINE_ITEMS,
    PROD_STRIPE_PLANS_LINE_ITEMS,
)
from api.common.services.mongodb.mongodb_service import get_db
from api.common.utils.utils import get_proper_user_data
from api.common.services.webhook.webhook_service import WebhookService
from api.common.services.payment.payment_service import PaymentService

endpoint_secret = os.environ.get("STRIPE_WEBHOOK_ENDPOINT_SECRET")


def configure_v1_routes(app):
    @app.route("/v1/search", methods=["GET"], endpoint="search_transcriptions")
    @requires_auth
    @requires_payment
    def search_transcriptions():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        try:
            return SearchController().search_transcriptions(search=search)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/search_by_video",
        methods=["GET"],
        endpoint="search_transcriptions_by_video",
    )
    @requires_auth
    @requires_payment
    def search_transcriptions_by_video():
        query_text = request.args.get("text", "")
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)

        search = SearchDTO(query_text, page, per_page)

        try:
            # Decoding JWT token and retrieving email attribute
            current_user = get_jwt_identity()
            email = current_user.get("email") if current_user else None

            # Printing email if page is equal to 1
            if page == 1:
                print(f"{email} - searched '{query_text}'")

            return SearchController().search_transcriptions_by_video(search=search)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/login",
        methods=["POST"],
        endpoint="login",
    )
    def login():
        json = request.get_json()
        email = json["email"]
        password = json["password"]

        login = PasswordLoginDTO(email, password)

        try:
            return UserController().password_login(login=login)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/forgot-password",
        methods=["POST"],
        endpoint="forgot-password",
    )
    def forgot_password():
        json = request.get_json()
        email = json["email"]
        try:
            return UserController().forgot_password(email=email)
        except Exception as e:
            print(e)
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/password-reset",
        methods=["POST"],
        endpoint="password-reset",
    )
    def password_reset():
        json = request.get_json()
        token = json["token"]
        password = json["password"]

        try:
            return UserController().password_reset(token=token, new_password=password)
        except Exception as e:
            print(e)
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @requires_auth
    @app.route("/v1/refresh", methods=["GET"], endpoint="refresh")
    def refresh_token():
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        current_user = get_db().users.find_one(current_user["_id"])
        user_data = get_proper_user_data(current_user)

        # Return the access token as a JSON response
        try:
            return jsonify({"access_token": create_access_token(user_data)})
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/google_login",
        methods=["POST"],
        endpoint="google_login",
    )
    def google_login():
        json = request.get_json()
        name = json["name"]
        picture = json["picture"]
        email = json["email"]
        id_token = json["id_token"]

        login = GoogleLoginDTO(name, picture, email, id_token)

        try:
            print(f"{email} - logged with google")
            return UserController().google_login(login=login)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @app.route(
        "/v1/register",
        methods=["POST"],
        endpoint="register",
    )
    def register():
        json = request.get_json()
        name = json["name"]
        email = json["email"]
        password = json["password"]

        register = UserDTO(name, email, password)

        try:
            print(f"{email} - registered with password")
            return UserController().register_w_password(register=register)
        except Exception as e:
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )

    @requires_auth
    @app.route("/checkout", methods=["POST"])
    def create_checkout_session():
        json = request.get_json()
        subscription_type = json["subscription_type"]
        customer_email = json["customer_email"]

        # Implement logic to create a checkout session with Stripe.
        # Return the session ID to the frontend.
        try:
            session = PaymentService().make_checkout(customer_email, subscription_type)
            print(
                f"{customer_email} - started the checkout session using the {subscription_type} plan"
            )
            return jsonify({"sessionId": session.id})
        except Exception as e:
            return jsonify({"error": str(e)}), 403

    @requires_auth
    @app.route("/cancel", methods=["POST"])
    def cancel_plan():
        json = request.get_json()
        customer_email = json["customer_email"]

        db = get_db()
        user = db.users.find_one({"email": customer_email})
        subscription_id = user["subscription"]["id"]

        try:
            PaymentService().change_subscription(
                subscription_id,
                {
                    "cancel_at_period_end": True,
                    "cancellation_details": {"comment": "Cancelled via backend"},
                },
            )
            print(
                f"{customer_email} - cancelled the subscription - id {subscription_id}"
            )
            return jsonify({"access_token": "Plan cancelled"})
        except Exception as e:
            return jsonify({"error": str(e)}), 403

    @requires_auth
    @app.route("/webhook", methods=["POST"])
    def webhook():
        event = request.json
        try:
            WebhookService(event).handle_events()
            return jsonify(success=True)
        except Exception as e:
            print(f" Webhook error {e}")
            return Response(
                response=str(e),
                status=500,
                mimetype="application/json",
            )
