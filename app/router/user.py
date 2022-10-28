from http import HTTPStatus
from smtplib import SMTPException

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.logger import log
from app.config import settings
from app.controller import send_email
from app import schema, oauth2
from app import model as m
from app.database import get_db

router = APIRouter(prefix="/user", tags=["Users"])


@router.get("/{id}", response_model=schema.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Gets user by

    Args:
        id (int): ID of user
        db (Session, optional):  Database sesion

    Raises:
        HTTPException: 404 - Not Found

    Returns:
        User: User's instance
    """
    user = db.query(m.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user


@router.post("/reset_password", status_code=HTTPStatus.OK)
def reset_password(data: schema.ResetPasswordData, db: Session = Depends(get_db)):
    """Resetting user password

    Args:
        id (int): ID of user
        db (Session, optional):  Database sesion

    Raises:
        HTTPException: 404 - Not Found

    Returns:
        User: User's instance
    """

    user: m.User = (
        db.query(m.User).filter_by(verification_token=data.verification_token).first()
    )
    if not user:
        log(
            log.WARNING,
            "User does not exist or token expired - [%s]",
            data.verification_token,
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    user.password = data.password
    user.verification_token = m.gen_uid()
    user.is_verified = True
    db.commit()
    return {"message": "Password has been updated"}


@router.post("/forgot_password", status_code=HTTPStatus.OK)
async def forgot_password(email: schema.EmailSchema, db: Session = Depends(get_db)):
    """Route for the case when the user has been already registered
    but forgot the password So email with the link for resetting the password will be sent

    Args:
        email (schema.EmailSchema): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user: m.User = db.query(m.User).filter_by(email=email.email).first()
    if not user:
        log(
            log.WARNING,
            "User does not exist - [%s]",
            email.email,
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    try:
        await send_email(
            user.email,
            user.username,
            f"{settings.FRONTEND_BASE_URL}/reset_password/{user.verification_token}",
        )
    except SMTPException as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f"Error send e-mail: {e}",
        )
    return HTTPStatus.OK


@router.get("/keys/google", response_model=schema.GooglKeys)
async def user_google_key(db: Session = Depends(get_db)):
    return {
        "google_client_id": settings.REACT_APP_GOOGLE_CLIENT_ID,
        "google_api_key": settings.REACT_APP_GOOGLE_API_KEY,
    }


@router.get("/keys/stripe", response_model=schema.StripeKey)
async def user_stripe_key(
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    current_user
    return {"stripe_public_key": settings.STRIPE_PUBLISHABLE_KEY}
