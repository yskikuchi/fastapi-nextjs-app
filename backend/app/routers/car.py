from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic.types import UUID4

import app.schemas.car as car_schema
import app.cruds.car as car_crud
import app.models.admin as admin_model
import app.services.auth_service as auth_service

from app.db.db import get_db

router = APIRouter(tags=["cars"])


@router.get("/cars", response_model=List[car_schema.Car])
async def get_cars(db: AsyncSession = Depends(get_db)):
    return await car_crud.get_cars(db)


@router.post("/cars")
async def create_booking(
    car_body: car_schema.CarCreate,
    db: AsyncSession = Depends(get_db),
    current_admin: admin_model.Admin = Depends(auth_service.get_current_user),
):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return await car_crud.create_car(car_body, db)


@router.patch("/cars/{car_id}")
async def update_car(
    car_id: UUID4,
    car_body: car_schema.CarUpdate,
    db: AsyncSession = Depends(get_db),
    current_admin: admin_model.Admin = Depends(auth_service.get_current_user),
):
    if not current_admin:
        raise HTTPException(status_code=401, detail="Unauthorized")

    original_car = await car_crud.get_car_by_id(car_id, db)
    if not original_car:
        raise HTTPException(status_code=404, detail="Car not found")

    return await car_crud.update_car(car_body, original_car, db)
