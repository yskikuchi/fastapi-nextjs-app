import uuid
import datetime

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy_utils import UUIDType
from sqlalchemy.orm import relationship
from app.db.db import Base


# 車両予約情報
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    # 予約照会番号
    reference_number = Column(String(1024), unique=True, nullable=False)
    # 利用開始時間
    start_time = Column(DateTime, nullable=False)
    # 利用終了時間
    end_time = Column(DateTime, nullable=False)
    # 予約金額(上限金額: 10,000,000円)
    amount = Column(Integer, nullable=False)
    # 予約ステータス(unconfirmed, confirmed, canceled, paid, completed)
    status = Column(String(1024), server_default="unconfirmed", nullable=False)
    user_id = Column(UUIDType(binary=False), ForeignKey("users.id"), nullable=False)
    car_id = Column(UUIDType(binary=False), ForeignKey("cars.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
    user = relationship("User", back_populates="booking")
