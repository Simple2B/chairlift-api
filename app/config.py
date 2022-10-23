from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    JWT_SECRET: str="secret"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30

    DATABASE_URI: str="sqlite:///./test.db"
    DEV_DATABASE_URI: str=""

    ADMIN_USER: str="admin"
    ADMIN_PASS: str="admin"
    ADMIN_EMAIL: EmailStr="admin@unknown.li"

    # SMTP client
    MAIL_USERNAME: str = "!unknown!"
    MAIL_PASSWORD: str = ""
    MAIL_FROM: EmailStr = "no@set.val"
    MAIL_PORT: int = 0
    MAIL_SERVER: str = ""
    MAIL_FROM_NAME: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
