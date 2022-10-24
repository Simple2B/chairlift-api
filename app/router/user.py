from http import HTTPStatus

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from app import model, schema, oauth2
from app.database import get_db


from app.logger import log

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
    """Gets user

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
