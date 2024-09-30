from pydantic import BaseModel, UUID4, Field, EmailStr
from datetime import datetime

from app.schemas.user import UserBase
from app.schemas.car import Car


class BookingBase(BaseModel):
    pass


# postで受け取るデータ
class BookingCreate(BookingBase):
    user: UserBase
    car_id: UUID4
    start_time: datetime = Field(
        None, json_schema_extra={"example": "2024-10-01T10:00:00"}
    )
    end_time: datetime = Field(
        None, json_schema_extra={"example": "2024-10-03T19:00:00"}
    )

    # フロント側で計算した金額?
    amount: int


class BookingReference(BookingBase):
    email: EmailStr
    reference_number: str


class BookingReferenceResponse(BookingBase):
    start_time: datetime
    end_time: datetime
    amount: int
    car: Car


class BookingCreateResponse(BookingBase):
    reference_number: str
