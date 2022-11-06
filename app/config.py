from functools import lru_cache
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    JWT_SECRET: str = "secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # TODO Remove DATABASE_URI
    DATABASE_URI: str = "sqlite:///./test.db"
    DB_URI: str
    DEV_DATABASE_URI: str = ""

    ADMIN_USER: str = "admin"
    ADMIN_PASS: str = "admin"
    ADMIN_EMAIL: EmailStr

    # SMTP client
    MAIL_USERNAME: str = "!unknown!"
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = "no@set.val"
    MAIL_PORT: int = 0
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = ""

    # Testing
    TEST_SEND_EMAIL: bool = False
    TEST_TARGET_EMAIL: str = "test@test.com"

    FRONTEND_BASE_URL: str = "http://localhost:3000"

    STRIPE_PUBLISHABLE_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""

    REACT_APP_GOOGLE_CLIENT_ID: str = ""
    REACT_APP_GOOGLE_API_KEY: str = ""

    GW_TCP_SERVER_PORT: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = Settings()
