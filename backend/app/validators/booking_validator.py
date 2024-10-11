from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

import app.models.booking as booking_model


async def validate_booking_overlap(create_booking, db: AsyncSession):
    existing_booking = await db.execute(
        select(booking_model.Booking).filter(
            booking_model.Booking.car_id == create_booking.car_id,
            booking_model.Booking.start_time < create_booking.end_time,
            booking_model.Booking.end_time > create_booking.start_time,
        )
    )
    if existing_booking.scalars().first():
        raise HTTPException(
            status_code=422, detail="選択した時間帯で既に予約が入っています"
        )
