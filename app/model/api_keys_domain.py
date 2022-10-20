from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from app.database import Base


class APIKeyDomain(Base):
    """
    Model that stores domain of key

    Args:

        (id): Identification field
        (key_id): Foreign Key on API Key model
        (domain): The name of the domain

    """

    __tablename__ = "api_keys_domains"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    key_id = Column(Integer, ForeignKey("api_keys.id"))

    domain = Column(String(256))
