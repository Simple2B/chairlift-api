from http import HTTPStatus
from smtplib import SMTPException

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app.logger import log
from app.config import settings
from app.controller import send_email
from app import model, schema, oauth2
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
    user = db.query(model.User).get(id)

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

    user: model.User = (
        db.query(model.User)
        .filter_by(verification_token=data.verification_token)
        .first()
    )
    if not user:
        log(
            log.WARNING,
            "User does not exist or token expired - [%s]",
            data.verification_token,
        )
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    user.password = data.password
    user.verification_token = ""
    user.is_verified = True
    db.commit()
    return {"message": "Password has been updated"}


@router.post("/forgot_password", status_code=HTTPStatus.OK)
async def forgot_password(email: schema.EmailSchema, db: Session = Depends(get_db)):
    user: model.User = db.query(model.User).filter_by(email=email.email).first()
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
