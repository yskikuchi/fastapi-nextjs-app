from app.core.config import settings


class Hash:
    def get_password_hash(password: str):
        return settings.pwd_context.hash(password)

    def verify_password(plain_password: str, hashed_password: str):
        return settings.pwd_context.verify(plain_password, hashed_password)
