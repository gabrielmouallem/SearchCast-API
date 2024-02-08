from api.common.services.mongodb.mongodb_service import get_db
from api.common.services.payment.payment_service import PaymentService


class WebhookService:

    def __init__(self, event):
        self.event = event

    def _handle_checkout_event(self):
        db = get_db()
        session = self.event["data"]["object"]
        db.checkouts.insert_one({**session, "_id": session["id"]})

    def _handle_subscription_event(self):
        db = get_db()
        subscription = self.event["data"]["object"]

        found_subscription = db.subscriptions.find_one({"_id": subscription["id"]})

        if found_subscription is not None:
            db.subscriptions.update_one(
                {"_id": subscription["id"]}, {"$set": subscription}
            )
        else:
            db.subscriptions.insert_one({**subscription, "_id": subscription["id"]})

        customer = PaymentService().get_customer(
            subscription["customer"]
        )  # PaymentService

        email = customer.email
        db.users.update_one(
            {"email": email},
            {"$set": {"subscription": subscription}},
        )

    def handle_events(self):
        if self.event["type"] == "checkout.session.completed":
            print(f'====> {self.event["type"]} triggered!')
            self._handle_checkout_event()

        elif self.event["type"] in [
            "customer.subscription.created",
            "customer.subscription.updated",
            "customer.subscription.deleted",
        ]:
            print(f'====> {self.event["type"]} triggered!')
            self._handle_subscription_event()

        else:
            print(f"Unhandled event type {self.event['type']}")
