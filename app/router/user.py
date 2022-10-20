from http import HTTPStatus

from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import model, schema, oauth2
from app.database import get_db


from app.logger import log

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    """Creates a new user instance and sends him

    Args:
        user (schema.UserCreate): Gets user's data
        db (Session, optional): Database sesion

    Raises:
        HTTPException: 409 Conflict

    Returns:
        _type_: A new user instance
    """

    new_user = model.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        if db.query(model.User).filter_by(email=user.email).first():
            log(
                log.ERROR,
                "User with such email [%s] - exists",
                user.email,
            )
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email already exists"
            )

        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=f"Database commit error: {e}",
        )

    db.refresh(new_user)
    log(log.INFO, "User [%s] - created", user.email)
    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    """Gets user

    Args:
        id (int): ID of user
        db (Session, optional):  Database sesion

    Raises:
        HTTPException: 404 - Not Found

    Returns:
        user: User instance
    """
    user = db.query(model.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user


@router.get("/reset_password", status_code=HTTPStatus.OK)
def reset_password(data: schema.ResetPasswordData, db: Session = Depends(get_db)):
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
    user.verification_token = None
    user.is_verified = True
    db.commit()

    return {"message": "Password has been updated"}
