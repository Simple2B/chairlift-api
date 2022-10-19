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
    """
    Model that describes API key

    Args:

        (id): Identification field
        (group_id): Foreign key on Group model
        (name): Name of current API key
        #TODO sensor_role
        #TODO group_role
        (key_hash): Hash of api key
        (created_at): Timestamp for current API key

    """

    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    name = Column(String(256), nullable=False)

    sensor_role = Column(Enum(Role), default=Role.NoneRole)
    group_role = Column(Enum(Role), default=Role.NoneRole)

    key_hash = Column(String(256))

    created_at = Column(DateTime(), default=datetime.now)
