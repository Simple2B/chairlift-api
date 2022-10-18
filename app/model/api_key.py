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


class APIKey(Base):
    __tablename__ = "api_key"

    id = Column(Integer, primary_key=True)

    group_id = Column(Integer, ForeignKey("group.id"))

    name = Column(String(256))

    sensor_role = Column(Enum(Role))
    group_role = Column(Enum(Role))

    key_hash = Column(String(256))

    created_at = Column(DateTime(), default=datetime.now)
