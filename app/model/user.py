import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime, func, or_, Enum

from app.hash_utils import make_hash, hash_verify
from app.database import Base, SessionLocal
from .role import Role


def gen_uid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), default=gen_uid)
    username = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    password_hash = Column(String(256), nullable=False)

    picture = Column(String(256), nullable=True)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime(), default=datetime.now)

    role = Column(Enum(Role), default=Role.NoneUser)

    google_openid_key = Column(String(256), nullable=True)
    apple_openid_key = Column(String(256), nullable=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db: SessionLocal, user_id: str, password: str):
        user = (
            db.query(cls)
            .filter(
                or_(
                    func.lower(cls.username) == func.lower(user_id),
                    func.lower(cls.email) == func.lower(user_id),
                )
            )
            .first()
        )
        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.username}>"
