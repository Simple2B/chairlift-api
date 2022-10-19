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
    __tablename__ = "group_invite_codes"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    invite_code = Column(String(256), nullable=False)

    expiration_date = Column(DateTime(), default=datetime.now)
    invitation_date = Column(DateTime(), default=datetime.now)

    group_role = Column(Enum(Role), default=Role.NoneRole, nullable=False)
    sensor_role = Column(Enum(Role), default=Role.NoneRole, nullable=False)

    email = Column(String(128), nullable=False)

    invited_by_user = Column(Integer, ForeignKey("users.id"))
