from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app import schema as s
from app.database import get_db
from app import model as m
from app.oauth2 import create_access_token
from app.logger import log
from app.controller import MailClient, get_mail_client
from app.config import Settings, get_settings

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=s.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Route that logins user and returns him a token
    ATTENTION: WE ONLY USE EMAIL TO AUTHENTICATE USER


    Args:
        user_credentials (OAuth2PasswordRequestForm, optional): Credentials of a user
        db (Session, optional): Database sesion

    Raises:
        HTTPException: 403 - Invalid Credentials

    Returns:
        json: Token for the new user and token type
    """
    user: m.User = m.User.authenticate(
        db,
        user_credentials.username,
        user_credentials.password,
    )

    if not user:
        log(log.WARNING, "User [%s] does not exist \n", user_credentials.username)
        raise HTTPException(status_code=404, detail="User not found")

    if not user.is_verified:
        log(log.WARNING, "User [%s] user is not verified", user)
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail="User is not verified"
        )

    access_token = create_access_token(data={"user_id": user.id})
    log(log.INFO, "Token for user [%s] has been generated", user.email)

    user_data = {
        "username": user.username,
        "email": user.email,
        "picture": user.picture,
        "is_deleted": user.is_deleted,
        "created_at": user.created_at,
        "role": user.role,
    }
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user_data,
    }


@auth_router.post("/google_login", response_model=s.Token)
def google_login(
    user_data: s.UserGoogleLogin,
    db: Session = Depends(get_db),
):
    """
    Route that logins user via the Google OAuth and returns him a token

    Args:
        user_data (OAuth2PasswordRequestForm, optional): Credentials of a user that google provides
        db (Session, optional): Database sesion

    Returns:
        json: Token for the new usesr and token type

    """
    user = db.query(m.User).filter_by(email=user_data.email).first()
    if not user:
        log(
            log.INFO,
            "User does not exist \n Creating user [%s] using Google OAuth",
            user_data.email,
        )
        user = m.User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.google_openid_key,
            google_openid_key=user_data.google_openid_key,
            picture=user_data.picture,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token(data={"user_id": user.id})
    log(log.INFO, "Token for user [%s] has been generated", user_data.email)

    user.picture = user_data.picture
    db.add(user)
    db.commit()
    db.refresh(user)

    user = {
        "username": user.username,
        "email": user.email,
        "picture": user.picture,
        "is_deleted": user.is_deleted,
        "created_at": user.created_at,
        "role": user.role,
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@auth_router.post("/sign_up", status_code=HTTPStatus.OK)
async def sign_up(
    user_data: s.UserSignUp,
    request: Request,
    db: Session = Depends(get_db),
    mail_client: MailClient = Depends(get_mail_client),
    settings: Settings = Depends(get_settings),
):
    """Signining up a new user

    Args:
        user_data (s.UserSignUp): Gets email and username
        request (Request): request
        db (Session, optional): Database sesion

    Raises:
        HTTPException: 422 - Error while sending email

    Returns:
        HTTP Status: 200 - OK
    """

    user = m.User(password="*", **user_data.dict())
    db.add(user)

    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "SQLAlchemyError:[%s]", e)
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Email already exists"
        )

    db.refresh(user)

    try:
        await mail_client.send_email(
            user.email,
            user.username,
            f"{settings.FRONTEND_BASE_URL}/reset_password/{user.verification_token}",
        )
    except Exception as e:
        log(log.ERROR, "Error: [%s]", e)
        db.delete(user)
        db.commit()

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f"Error send e-mail: {e}",
        )

    db.commit()
    return HTTPStatus.OK
