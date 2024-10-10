from pydantic import BaseModel, UUID4, Field, EmailStr, field_validator
from typing import Literal
from datetime import datetime, timedelta

from app.schemas.user import UserBase
from app.schemas.car import Car


class BookingBase(BaseModel):
    pass


# postで受け取るデータ
class BookingCreate(BookingBase):
    user: UserBase
    car_id: UUID4

    start_time: datetime = Field(
        None,
        json_schema_extra={
            "example": (datetime.now() + timedelta(days=2)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        },
    )
    end_time: datetime = Field(
        None,
        json_schema_extra={
            "example": (datetime.now() + timedelta(days=4)).strftime(
                "%Y-%m-%dT%H:%M:%S"
            )
        },
    )

    # フロント側で計算した金額?
    amount: int = Field(None, json_schema_extra={"example": 10000}, ge=0, le=10000000)

    @field_validator("start_time", "end_time", mode="before")
    def time_must_be_in_future(cls, v):
        parsed_time = datetime.fromisoformat(v) if isinstance(v, str) else v
        if parsed_time < datetime.now():
            raise ValueError("未来の日付を指定してください")
        return v

    @field_validator("end_time")
    def end_must_be_after_start(cls, v, values):
        start_time = (
            datetime.fromisoformat(values.data["start_time"])
            if isinstance(values.data["start_time"], str)
            else values.data["start_time"]
        )
        end_time = datetime.fromisoformat(v) if isinstance(v, str) else v
        if start_time >= end_time:
            raise ValueError("利用終了時間は利用開始時間より後にしてください")
        return v


class BookingReference(BookingBase):
    email: EmailStr
    reference_number: str


class BookingReferenceResponse(BookingBase):
    start_time: datetime
    end_time: datetime
    amount: int
    status: Literal["unconfirmed", "confirmed", "canceled", "paid", "completed"]
    car: Car


class BookingCreateResponse(BookingBase):
    reference_number: str
