from pydantic import (
    BaseModel,
    UUID4,
    Field,
    EmailStr,
    model_validator,
    field_validator,
    ConfigDict,
)
from pydantic.alias_generators import to_camel
from typing import Literal
from datetime import datetime, timedelta

from app.schemas.user import UserBase
from app.schemas.car import Car
from app.types.status import BookingStatus


class BookingBase(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)


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
    @classmethod
    def time_must_be_in_future(cls, v):
        parsed_time = datetime.fromisoformat(v) if isinstance(v, str) else v
        if parsed_time < datetime.now():
            raise ValueError("未来の日付を指定してください")
        return v

    @model_validator(mode="after")
    def validate_time_range(self):
        start_time = self.start_time
        end_time = self.end_time
        if start_time >= end_time:
            raise ValueError("利用終了時間は利用開始時間より後にしてください")
        return self


class BookingReference(BookingBase):
    email: EmailStr
    reference_number: str


class BookingReferenceResponse(BookingBase):
    start_time: datetime
    end_time: datetime
    amount: int
    status: BookingStatus
    car: Car


class BookingCreateResponse(BookingBase):
    reference_number: str


class Booking(BookingBase):
    id: UUID4
    user: UserBase
    car: Car
    start_time: datetime
    end_time: datetime
    amount: int
    status: BookingStatus
    reference_number: str
    created_at: datetime
    updated_at: datetime
