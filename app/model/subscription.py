from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Subscription(Base):
    """Model that stores subscription data for the user

    Args:

        (id): Identification field
        (user_id): Foreign Key on User id
        (is_active): A value that determines whether the user will
        have the functionality available by subscription or not

    """

    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    is_active = Column(Boolean, default=False)

    created_at = Column(DateTime(), default=datetime.now)

    user = relationship("User")
