import random
import string
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import joinedload
from pydantic.types import UUID4

import app.schemas.booking as booking_schema
import app.models.booking as booking_model
import app.models.user as user_model
import app.models.car as car_model


async def search_booking(
    search_body: booking_schema.BookingReference, db: AsyncSession
) -> booking_schema.BookingReferenceResponse:
    # 予約照会番号とメールアドレスで予約を検索
    result = await db.execute(
        select(booking_model.Booking, car_model.Car)
        .join(user_model.User)
        .join(car_model.Car)
        .filter(
            booking_model.Booking.reference_number == search_body.reference_number,
            user_model.User.email == search_body.email,
        )
    )
    if not result:
        return None

    booking_info, car_info = result.first()
    return {
        "start_time": booking_info.start_time,
        "end_time": booking_info.end_time,
        "amount": booking_info.amount,
        "status": booking_info.status,
        "car": {
            "id": car_info.id,
            "name": car_info.name,
            "capacity": car_info.capacity,
            "car_number": car_info.car_number,
        },
    }


async def create_booking(
    create_booking: booking_schema.BookingCreate, db: AsyncSession, user_id: UUID4
) -> booking_schema.BookingCreateResponse:
    try:
        reference_number = await generate_reference_number(db)
        booking = booking_model.Booking(
            **create_booking.model_dump(exclude={"user"}),
            reference_number=reference_number,
            user_id=user_id
        )
        db.add(booking)
        await db.commit()
        await db.refresh(booking)
    except Exception as e:
        db.rollback()
        raise e

    return {"reference_number": booking.reference_number}


async def approve_booking(db: AsyncSession, original_booking: booking_model.Booking):
    original_booking.status = "confirmed"
    db.add(original_booking)
    await db.commit()
    await db.refresh(original_booking)
    return {"message": "Confirmed"}


async def get_booking_with_user(booking_id: UUID4, db: AsyncSession):
    result = await db.execute(
        select(booking_model.Booking)
        .filter(booking_model.Booking.id == booking_id)
        .options(joinedload(booking_model.Booking.user))
    )

    booking = result.first()
    return booking[0] if booking is not None else None


# 予約照会番号としてランダムな文字列を生成
async def generate_reference_number(db: AsyncSession) -> str:
    # 最大試行回数を設定
    max_attempts = 5
    attempts = 0
    while attempts < max_attempts:
        random_number = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        result = await db.execute(
            select(booking_model.Booking).filter_by(reference_number=random_number)
        )
        existing_booking = result.scalars().first()
        if not existing_booking:
            return random_number
        attempts += 1

    raise Exception("Failed to generate a unique reference number")
