from typing import List
from pydantic.types import UUID4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.engine import Result

import app.schemas.user as user_schema
import app.models.user as user_model


async def create_user(create_user: user_schema.UserBase, db: AsyncSession) -> UUID4:
    # 予約者情報をusersテーブルに登録
    user = user_model.User(**create_user.model_dump())
    db.add(user)
    await db.flush()  # flush()を使って、DBにデータを保存する前に、user.idを取得

    return user.id
