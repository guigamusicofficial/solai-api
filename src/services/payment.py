import stripe
from src.config import settings
from src.models.user import User
from src.models.subscription import Plan

stripe.api_key = settings.stripe_secret_key

class StripeService:
    async def create_checkout_session(self, user: User, plan: Plan):
        """
        Create a Stripe checkout session for subscription.
        """
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": plan.stripe_price_id,
                        "quantity": 1,
                    }
                ],
                mode="subscription",
                success_url=f"{settings.frontend_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.frontend_url}/plans",
                customer_email=user.email,
                metadata={
                    "user_id": str(user.id),
                    "plan_id": str(plan.id)
                }
            )
            return session
        except Exception as e:
            print(f"Stripe error: {e}")
            raise
    
    async def handle_webhook(self, event: dict):
        """
        Handle Stripe webhook events.
        """
        if event["type"] == "checkout.session.completed":
            # Update subscription in database
            pass
        elif event["type"] == "customer.subscription.updated":
            pass
        elif event["type"] == "customer.subscription.deleted":
            pass
