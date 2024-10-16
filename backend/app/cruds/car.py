from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.engine import Result
from pydantic.types import UUID4

import app.schemas.car as car_schema
import app.models.car as car_model


async def get_cars(db: AsyncSession) -> List[car_model.Car]:
    result: Result = await db.execute(
        select(
            car_model.Car.id,
            car_model.Car.name,
            car_model.Car.capacity,
            car_model.Car.car_number,
            car_model.Car.price_for_initial_twelve_hours,
            car_model.Car.price_per_additional_six_hours,
        )
    )
    return result.all()


async def create_car(
    create_car: car_schema.CarCreate, db: AsyncSession
) -> car_schema.CarCreateResponse:
    car = car_model.Car(**create_car.model_dump())
    db.add(car)
    await db.commit()
    await db.refresh(car)
    return {"id": car.id}


async def update_car(
    update_car: car_schema.CarUpdate,
    original: car_model.Car,
    db: AsyncSession,
):
    original.capacity = update_car.capacity
    original.car_number = update_car.car_number
    original.name = update_car.name
    original.price_for_initial_twelve_hours = update_car.price_for_initial_twelve_hours
    original.price_per_additional_six_hours = update_car.price_per_additional_six_hours
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return {"message": "Updated"}


async def get_car_by_id(car_id: UUID4, db: AsyncSession) -> car_model.Car:
    result: Result = await db.execute(
        select(
            car_model.Car
        ).where(car_model.Car.id == car_id)
    )
    car = result.first()
    return car[0] if result is not None else None
