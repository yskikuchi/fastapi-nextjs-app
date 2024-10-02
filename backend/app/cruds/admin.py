from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from fastapi import HTTPException, Depends
from pydantic import EmailStr

import app.models.admin as admin_model
import app.schemas.admin as admin_schema
from app.core.hash import Hash
from app.services import auth_service


async def create_admin(db: AsyncSession, admin_create: admin_schema.AdminCreate):
    existing_admin = await check_admin(
        db,
        admin_create,
    )
    if existing_admin:
        raise HTTPException(
            status_code=400, detail="このメールアドレスは既に登録されています"
        )

    admin = admin_model.Admin(**admin_create.model_dump(exclude={"password"}))
    admin.password = Hash.get_password_hash(admin_create.password)

    db.add(admin)
    await db.commit()
    await db.refresh(admin)
    return {"message": "Created"}


async def login_admin(db: AsyncSession, email: EmailStr, password: str):
    admin = await authenticate_admin(db, email, password)
    return {
        "access_token": auth_service.create_access_token({"sub": admin.email}),
        "token_type": "bearer",
    }


async def authenticate_admin(db: AsyncSession, email: EmailStr, password: str):
    admin = await get_user_by_email(db, email)
    if not admin:
        raise HTTPException(
            status_code=401, detail="メールアドレスまたはパスワードが正しくありません"
        )

    if not Hash.verify_password(password, admin.password):
        raise HTTPException(
            status_code=401, detail="メールアドレスまたはパスワードが正しくありません"
        )

    return admin


async def get_user_by_email(db: AsyncSession, email: EmailStr):
    user = await db.execute(
        select(admin_model.Admin).where(admin_model.Admin.email == email)
    )
    return user.scalar()


async def check_admin(
    db: AsyncSession, admin_create: admin_schema.AdminCreate
) -> admin_model.Admin:
    checked_admin = await db.execute(
        select(admin_model.Admin).where(admin_model.Admin.email == admin_create.email)
    )

    return checked_admin.first()
