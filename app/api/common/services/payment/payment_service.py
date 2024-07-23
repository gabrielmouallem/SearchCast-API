import os
import stripe

DEV_STRIPE_PLANS_LINE_ITEMS = {
    "month": {
        "price": "price_1PfmJPAvzLrWK4UoMHHjVuoH",
        "quantity": 1,
    },
    "semester": {
        "price": "price_1PfmKjAvzLrWK4UoKB8bkIsj",
        "quantity": 1,
    },
    "year": {
        "price": "price_1PfmLCAvzLrWK4UoGdAuFtEI",
        "quantity": 1,
    },
}

PROD_STRIPE_PLANS_LINE_ITEMS = {
    "month": {
        "price": "price_1OZQCzAvzLrWK4Uo2GEDw2FH",
        "quantity": 1,
    },
    "semester": {
        "price": "price_1OZQChAvzLrWK4UoaX0hpjWd",
        "quantity": 1,
    },
    "year": {
        "price": "price_1OZQC9AvzLrWK4UogSbROUH9",
        "quantity": 1,
    },
}

FRONTEND_URL = os.environ.get("FRONTEND_URL")


class PaymentService:

    def get_customer(self, id):
        return stripe.Customer.retrieve(id)

    def make_checkout(self, customer_email, subscription_type):
        is_prod = os.environ.get("FLASK_ENV") == "deployment"
        return stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                (
                    PROD_STRIPE_PLANS_LINE_ITEMS[subscription_type]
                    if is_prod
                    else DEV_STRIPE_PLANS_LINE_ITEMS[subscription_type]
                )
            ],
            customer_email=customer_email,
            mode="subscription",
            success_url=f"{FRONTEND_URL}/search",  # Change to your success URL
            cancel_url=f"{FRONTEND_URL}/plans",  # Change to your cancel URL
        )

    def change_subscription(self, id, rest):
        stripe.Subscription.modify(id, **rest)
