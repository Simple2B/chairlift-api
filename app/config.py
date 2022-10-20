from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    DATABASE_URI: str
    DEV_DATABASE_URI: str
    DB_URI: str

    ADMIN_USER: str
    ADMIN_PASS: str
    ADMIN_EMAIL: EmailStr

    # SMTP client
    MAIL_USERNAME: str = "!unknown!"
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str

    FRONTEND_RESET_PASSWORD_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
