from fastapi import HTTPException, Depends, APIRouter
from app import model, schema, oauth2
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    new_user = model.User(**user.dict())
    db.add(new_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        if db.query(model.User).filter_by(username=user.username).first():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Username already exists"
            )
        if db.query(model.User).filter_by(email=user.email).first():
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email already exists"
            )

    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user = db.query(model.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user
