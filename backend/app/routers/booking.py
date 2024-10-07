from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.booking as booking_schema
import app.cruds.booking as booking_crud
import app.cruds.user as user_crud
from app.db.db import get_db
import app.services.mail_service as mail_service
import app.services.auth_service as auth_service
import app.services.stripe_service as stripe_service
import app.models.admin as admin_model
import stripe

router = APIRouter(tags=["booking"])


@router.post("/booking", response_model=booking_schema.BookingCreateResponse)
async def create_booking(
    booking_body: booking_schema.BookingCreate, db: AsyncSession = Depends(get_db)
):
    user_id = await user_crud.create_user(booking_body.user, db)
    response = await booking_crud.create_booking(booking_body, db, user_id)

    await mail_service.send_email(
        ["admin@sample.com"],
        "予約リクエスト",
        {
            "name": booking_body.user.name,
            "email": booking_body.user.email,
            "start_time": booking_body.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": booking_body.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        },
        "request_notice.html",
    )
    return response


@router.patch("/booking/{booking_id}/approve")
async def approve_booking(
    booking_id: UUID4,
    db: AsyncSession = Depends(get_db),
    current_admin: admin_model.Admin = Depends(auth_service.get_current_user),
):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    booking = await booking_crud.get_booking_with_user(booking_id, db)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    response = await booking_crud.approve_booking(db, booking)

    # Stripe決済リンクの生成
    payment_link = await stripe_service.create_stripe_payment_link(
        booking.amount, str(booking.reference_number)
    )

    await mail_service.send_email(
        [booking.user.email],
        "予約確定",
        {"payment_link": payment_link},
        "approval_notice.html",
    )
    return response


@router.post("/booking/search", response_model=booking_schema.BookingReferenceResponse)
async def search_booking(
    search_body: booking_schema.BookingReference, db: AsyncSession = Depends(get_db)
):
    return await booking_crud.search_booking(search_body, db)


# 支払いイベントを処理
@router.post("/booking/payment/webhook")
async def handle_payment_event(request: Request, db: AsyncSession = Depends(get_db)):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = None

    endpoint_secret = (
        "whsec_779693f0c5743417e69c6a80a12864c071909f760849e335424feea604ac3f23"
    )

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        # Invalid payload
        return HTTPException(status_code=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HTTPException(status_code=400)

    # 支払い完了後にpaidステータスに更新
    if event["type"] == "checkout.session.completed":
        await stripe_service.fullfill_checkout(event["data"]["object"]["id"], db)

    return HTTPException(status_code=200)
