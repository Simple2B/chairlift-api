from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Enum,
)
from .role import Role
from app.database import Base


class GroupInviteCode(Base):
    __tablename__ = "group_invite_code"

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey("group.id"))

    invite_code = Column(String(256))

    expiration_date = Column(DateTime(), default=datetime.now)
    invitation_date = Column(DateTime(), default=datetime.now)

    group_role = Column(Enum(Role))
    sensor_role = Column(Enum(Role))

    email = Column(String(128))

    invited_by_user = Column(Integer, ForeignKey("user.id"))
