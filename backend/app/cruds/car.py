from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.engine import Result

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
