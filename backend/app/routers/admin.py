from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db import get_db
import app.cruds.admin as admin_crud
import app.schemas.admin as admin_schema

router = APIRouter(tags=["admin"])


@router.post("/admin")
async def create_admin(
    admin_create: admin_schema.AdminCreate,
    db: AsyncSession = Depends(get_db),
):
    return await admin_crud.create_admin(db, admin_create)


@router.post("/admin/login")
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    return await admin_crud.login_admin(db, form_data.username, form_data.password)
