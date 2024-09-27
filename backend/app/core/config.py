import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

load_dotenv()


class Settings:
    AUTH_API_PROJECT_NAME: str = "Application"
    AUTH_API_PROJECT_VERSION: str = "0.1.0"
    AUTH_API_DESCRIPTION: str = """
  アプリケーションに関する説明などを記載（markdownで書けば、反映される）
  """

    # DB関連の設定
    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DOCKER: str = os.environ["POSTGRES_DOCKER"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_DOCKER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_schema = OAuth2PasswordBearer(tokenUrl="/user/token")


# インスタンス化
settings = Settings()
