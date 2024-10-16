import uuid
import datetime

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType

from app.db.db import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    # 車名
    name = Column(String(1024))
    # 定員
    capacity = Column(Integer)
    # 車両番号
    car_number = Column(String(1024))
    # 最初の12時間までの料金
    price_for_initial_twelve_hours = Column(Integer, nullable=False)
    # 以降6時間あたりの料金
    price_per_additional_six_hours = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    booking = relationship("Booking", back_populates="car")
