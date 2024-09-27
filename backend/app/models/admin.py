import uuid
import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy_utils import UUIDType

from app.db.db import Base

class Admin(Base):
    __tablename__ = "admins"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String(1024))
    email = Column(String(1024))
    password = Column(String(1024))
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now)
