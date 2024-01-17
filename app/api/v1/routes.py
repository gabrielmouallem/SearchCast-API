# routes.py
import os
from flask import Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import stripe
from api.common.decorators import requires_auth, requires_payment
from api.v1.search.dto import SearchDTO
from api.v1.search.controller import SearchController
from api.v1.auth.controller import UserController
from api.v1.auth.dto import GoogleLoginDTO, PasswordLoginDTO, UserDTO
from api.v1.webhook.constants import STRIPE_PLANS_LINE_ITEMS
from api.common.services.mongodb.mongodb_service import get_db
from api.common.utils.utils import get_proper_user_data

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

    @requires_auth
    @app.route("/v1/refresh", methods=["GET"], endpoint="refresh")
    def refresh_token():
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        current_user = get_db().users.find_one(current_user["_id"])
        user_data = get_proper_user_data(current_user)

        # Return the access token as a JSON response
        try:
            return jsonify({"access_token": user_data})
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
        family_name = json["family_name"]
        given_name = json["given_name"]
        email = json["email"]
        id_token = json["id_token"]

        login = GoogleLoginDTO(name, picture, family_name, given_name, email, id_token)

        try:
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
            frontend_url = os.environ.get("FRONTEND_URL")
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[STRIPE_PLANS_LINE_ITEMS[subscription_type]],
                customer_email=customer_email,
                mode="subscription",
                success_url=f"{frontend_url}/search?success=true",  # Change to your success URL
                cancel_url=f"{frontend_url}/plans?success=false",  # Change to your cancel URL
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
            stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True,
                cancellation_details={"comment": "Cancelled via backend"},
            )
            return jsonify({"access_token": "Plan cancelled"})
        except Exception as e:
            return jsonify({"error": str(e)}), 403

    @requires_auth
    @app.route("/webhook", methods=["POST"])
    def webhook():
        db = get_db()
        event = request.json

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            db.checkouts.insert_one({**session, "_id": session["id"]})

        elif event["type"] == "customer.subscription.created":
            handle_subscription_event(event)

        elif event["type"] == "customer.subscription.updated":
            handle_subscription_event(event)

        elif event["type"] == "customer.subscription.deleted":
            handle_subscription_event(event)

        else:
            print(f"Unhandled event type {event['type']}")

        return jsonify(success=True)


def handle_subscription_event(event):
    db = get_db()
    subscription = event["data"]["object"]
    db.subscriptions.insert_one({**subscription, "_id": subscription["id"]})

    customer = stripe.Customer.retrieve(subscription["customer"])

    email = customer.email
    db.users.update_one(
        {"email": email},
        {"$set": {"subscription": subscription}},
    )
