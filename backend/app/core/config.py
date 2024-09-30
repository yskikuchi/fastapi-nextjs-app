import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr

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

    MAIL_USERNAME: str = os.environ["MAIL_USERNAME"]
    MAIL_PASSWORD: str = os.environ["MAIL_PASSWORD"]
    MAIL_FROM: EmailStr = os.environ["MAIL_FROM"]
    MAIL_PORT: int = int(os.environ["MAIL_PORT"])
    MAIL_SERVER: str = os.environ["MAIL_SERVER"]
    MAIL_SSL_TLS: bool = os.environ["MAIL_SSL_TLS"]
    MAIL_STARTTLS: bool = os.environ["MAIL_STARTTLS"]
    USE_CREDENTIALS: bool = os.environ["USE_CREDENTIALS"]
    MAIL_FROM_NAME: str = None

# インスタンス化
settings = Settings()
