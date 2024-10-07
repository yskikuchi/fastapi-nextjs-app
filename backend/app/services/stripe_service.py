import stripe
import os
from sqlalchemy.ext.asyncio import AsyncSession
import app.cruds.booking as booking_crud

stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


async def create_stripe_payment_link(amount: int, reference_number: str) -> str:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "jpy",
                    "product_data": {
                        "name": f"予約照会番号: {reference_number}",
                    },
                    "unit_amount": amount,
                },
                "quantity": 1,
            }
        ],
        metadata={"reference_number": reference_number},
        mode="payment",
        # フロントエンドのURLを指定
        success_url=f"https://yourdomain.com/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url="https://yourdomain.com/cancel",
    )
    return session.url


async def fullfill_checkout(session_id: str, db: AsyncSession):
    session = stripe.checkout.Session.retrieve(
        session_id,
        expand=["line_items"],
    )

    booking = await booking_crud.get_booking_by_reference_number(
        session.metadata.reference_number, db
    )
    await booking_crud.complete_payment(db, booking)
