from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    LargeBinary,
)

from app.database import Base


class Firmware(Base):
    """
    Model for firware data

    Args:

        (id): Identification field
        (model): Firmware model name
        (hardware): Hadware
        (hash): Hash
        (date): Timestamp of firmware creation
        (data): Data
        (bin): Bin

    """

    __tablename__ = "firmwares"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    model = Column(String(128))

    hardware = Column(String(256))

    hash = Column(String(256))

    date = Column(DateTime(), default=datetime.now)

    data = Column(LargeBinary())
    bin = Column(LargeBinary())
