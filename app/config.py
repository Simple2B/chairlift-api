import os

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    JWT_SECRET: str = os.getenv("JWT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    DATABASE_URI: str = os.getenv("DEV_DATABASE_URI")
    DEV_DATABASE_URI: str = os.getenv("DEV_DATABASE_URI")
    DB_URI: str

    ADMIN_USER: str = os.getenv("PROD_DATABASE_URI")
    ADMIN_PASS: str = os.getenv("ADMIN_PASS")
    ADMIN_EMAIL: EmailStr = os.getenv("ADMIN_EMAIL")

    class Config:
        env_file = ".env"


settings = Settings()
