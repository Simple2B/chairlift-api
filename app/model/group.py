from datetime import datetime


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from .role import Role


class Group(Base):
    __tablename__ = "group"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))

    group_owner = Column(Integer, ForeignKey("user.id"))

    created_at = Column(DateTime(), default=datetime.now)

    # relationships

    # Gets all users who belong to this group
    users = relationship("User", secondary="user_group", backref="groups")

    # Gets all users that created THIS group
    user_owner = relationship("User", backref="own_groups")

    sensors = relationship("Sensor", secondary="sensor_group", backref="sensors")


class UserGroup(Base):
    __tablename__ = "user_group"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("user.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    sensor_role = Column(Enum(Role))
    group_role = Column(Enum(Role))

    joined_at = Column(DateTime(), default=datetime.now)


class SensorGroup(Base):
    __tablename__ = "sensor_group"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    edit_roles = Column(Enum(Role))
    view_roles = Column(Enum(Role))
    share_roles = Column(Enum(Role))

    joined_at = Column(DateTime(), default=datetime.now)
