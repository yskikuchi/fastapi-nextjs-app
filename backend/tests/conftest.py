import pytest
import os
import pytest_asyncio
from os.path import join, dirname
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.db import get_db, Base
from app.main import app
from dotenv import load_dotenv

# TODO: テスト用の環境変数を読み込めるようにする
# dotenv_path = join(dirname(__file__), ".env.test")
# load_dotenv(verbose=True, dotenv_path=".env.test")

# POSTGRES_USER: str = os.environ["POSTGRES_USER"]
# POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
# POSTGRES_DOCKER: str = os.environ["POSTGRES_DOCKER"]
# POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
# POSTGRES_DB: str = os.environ["POSTGRES_DB"]
TEST_DATABASE_URL = (
    f"postgresql+asyncpg://test:test_password@test_db:5432/booking_db_test"
)


@pytest_asyncio.fixture
async def async_session_fixture() -> AsyncSession:
    async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    async_engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
    )

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async def get_test_db():
        async with async_session() as db:
            yield db

    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


# テスト用の管理者ユーザーを作成し、ログインしてアクセストークンを返す
async def create_admin_and_login(async_client):
    name = "admin"
    email = "admin@example.com"
    password = "password"
    await async_client.post(
        "/admin",
        json={"name": name, "email": email, "password": password},
    )
    login_response = await async_client.post(
        "/admin/login", data={"username": email, "password": password}
    )
    return login_response.json()["access_token"]
