from pathlib import Path

from starlette.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app import schema as s
from app.config import settings

mail = FastMail(
    ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=False,
        TEMPLATE_FOLDER=Path("app/templates"),
    )
)


async def send_email(
    email: s.EmailListSchema,
    username: str,
    verification_link: str,
) -> JSONResponse:
    """
    Function for generating email

    Args:
        email (email.EmailListSchema): email string
        verification_link (str): link that will be integrated in email

    Returns:
        JSONResponse: Email has been spent
    """
    message = MessageSchema(
        subject="Account verification",
        recipients=[email],
        template_body={
            "username": username,
            "verification_link": verification_link,
        },
        subtype=MessageType.html,
    )

    await mail.send_message(message, template_name="email_template.html")
    return JSONResponse(
        status_code=200,
        content={
            "message": "email has been sent",
        },
    )
