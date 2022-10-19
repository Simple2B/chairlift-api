from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    DateTime,
    func,
    or_,
    Enum,
)

from app.hash_utils import make_hash, hash_verify
from app.database import Base, SessionLocal
from .role import Role


class User(Base):
    """
    Model that describes user

    Args:

        (id): Identification field
        (username): User's username
        (email): User's email
        (password): User's hashed password
        (picture): URL to picture
        (verified): Checks if user account verified by email or by OAuth provider
        (is_deleted): Checks if the user is deleted.In fact, we need this to maintain the integrity of the database
        (role): Assign role to current user
        (google_openid_key): Token that proves that user really got signied-in via Google
        (apple_openid_key): Token that proves that user really got signied-in via Apple

    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(64), nullable=False, unique=True, index=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    password_hash = Column(String(256), nullable=False)

    picture = Column(String(256), nullable=True)
    verified = Column(Boolean, default=False)

    is_deleted = Column(Boolean(), default=False)

    created_at = Column(DateTime(), default=datetime.now)

    role = Column(Enum(Role), default=Role.NoneRole)

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
