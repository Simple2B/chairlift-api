from datetime import datetime


from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum


from app.database import Base
from .role import Role


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    sensor_role = Column(Enum(Role), default=Role.User)
    group_role = Column(Enum(Role), default=Role.User)

    joined_at = Column(DateTime(), default=datetime.now)
