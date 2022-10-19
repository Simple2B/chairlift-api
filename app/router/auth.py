from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schema
from app.database import get_db
from app.model import User
from app.oauth2 import create_access_token

auth_router = APIRouter(tags=["Authentication"])


@auth_router.post("/login", response_model=schema.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        user_credentials (OAuth2PasswordRequestForm, optional): _description_. Defaults to Depends().
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user: User = User.authenticate(
        db,
        user_credentials.username,
        user_credentials.password,
    )

    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/google_login")
def google_login(user_data: schema.UserGoogleLogin, db: Session = Depends(get_db),):
    user_data

    user: User = User

    # if not user:
    #     raise HTTPException(status_code=403, detail="Invalid credentials")

    # access_token = create_access_token(data={"user_id": user.id})

    # return {"access_token": access_token, "token_type": "bearer"}
    # return 'ok'
