from datetime import datetime


from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.database import Base
from .role import Role


class Group(Base):
    """
    Model for Group

    Args:

        (id): Identification field
        (name): Name of the group
        (group_owner): Foreign Key on owner of current group
        (created_at): Date of group creation
        (users): Gets all groups the user is in
        (user_owner): Get all groups owned by (relates to the user)
        (sensors): Gets all sensors assigned to this group

    """

    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))

    group_owner = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime(), default=datetime.now)

    # relationships

    # Gets all users who belong to this group
    users = relationship("User", secondary="user_groups", backref="groups")

    # Gets all users that created THIS group
    user_owner = relationship("User", backref="own_groups")

    sensors = relationship("Sensor", secondary="sensor_groups", backref="sensors")


class UserGroup(Base):
    __tablename__ = "user_groups"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    sensor_role = Column(Enum(Role), default=Role.NoneRole)
    group_role = Column(Enum(Role), default=Role.NoneRole)

    joined_at = Column(DateTime(), default=datetime.now)


class SensorGroup(Base):
    __tablename__ = "sensor_groups"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    edit_roles = Column(Enum(Role), default=Role.NoneRole)
    view_roles = Column(Enum(Role), default=Role.NoneRole)
    share_roles = Column(Enum(Role), default=Role.NoneRole)

    joined_at = Column(DateTime(), default=datetime.now)
