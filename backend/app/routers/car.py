from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import app.schemas.car as car_schema
import app.cruds.car as car_crud

from app.db.db import get_db

router = APIRouter(tags=["cars"])


@router.get("/cars", response_model=List[car_schema.Car])
async def get_cars(db: AsyncSession = Depends(get_db)):
    return await car_crud.get_cars(db)


@router.post("/cars")
async def create_booking(
    car_body: car_schema.CarCreate, db: AsyncSession = Depends(get_db)
):
    return await car_crud.create_car(car_body, db)
