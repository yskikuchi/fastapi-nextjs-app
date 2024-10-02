from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.booking as booking_schema
import app.cruds.booking as booking_crud
import app.cruds.user as user_crud
from app.db.db import get_db
import app.services.mail_service as mail_service
import app.services.auth_service as auth_service
import app.models.admin as admin_model

router = APIRouter(tags=["booking"])


@router.post("/booking", response_model=booking_schema.BookingCreateResponse)
async def create_booking(
    booking_body: booking_schema.BookingCreate, db: AsyncSession = Depends(get_db)
):
    user_id = await user_crud.create_user(booking_body.user, db)
    response = await booking_crud.create_booking(booking_body, db, user_id)

    await mail_service.send_email(
        ["admin@sample.com"],
        {
            "name": booking_body.user.name,
            "email": booking_body.user.email,
            "start_time": booking_body.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": booking_body.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        },
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

    booking = await booking_crud.get_booking(booking_id, db)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return await booking_crud.approve_booking(db, booking)


@router.post("/booking/search", response_model=booking_schema.BookingReferenceResponse)
async def search_booking(
    search_body: booking_schema.BookingReference, db: AsyncSession = Depends(get_db)
):
    return await booking_crud.search_booking(search_body, db)
