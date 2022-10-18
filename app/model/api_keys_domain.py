from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from app.database import Base


class APIKeyDomain(Base):
    __tablename__ = "api_keys_domain"

    id = Column(Integer, primary_key=True)

    key_id = Column(Integer, ForeignKey("api_key.id"))

    domain = Column(String(256))
