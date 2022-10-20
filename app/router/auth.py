from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.config import settings
from app import schema as s
from app.database import get_db
from app import model as m
from app.oauth2 import create_access_token

from app.logger import log
from app.controller import send_email

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=s.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Route that logins user and returns him a token

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
    if not user.is_verified:
        log(log.WARNING, "User [%s] user is not verified", user)
        raise HTTPException(
            status_code=HTTPStatus.NOT_ACCEPTABLE, detail="User is not verified"
        )

    if not user:
        log(log.WARNING, "User [%s] does not exist \n", user_credentials.username)
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})
    log(log.INFO, "Token for user [%s] has been generated", user.email)
    return {"access_token": access_token, "token_type": "bearer"}


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
        user = s.UserCreate(
            username=user_data.username,
            email=user_data.email,
            password=user_data.google_openid_key,
            google_openid_key=user_data.google_openid_key,
        )
        user = m.User(**user.dict())
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token = create_access_token(data={"user_id": user.id})

    log(log.INFO, "Token for user [%s] has been generated", user_data.email)

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/sign_up", status_code=HTTPStatus.OK)
async def sign_up(user_data: s.UserSignUp, db: Session = Depends(get_db)):
    user = m.User(password="*", **user_data.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    await send_email(
        user.email, settings.FRONTEND_RESET_PASSWORD_URL + user.verification_token
    )
    return HTTPStatus.OK
