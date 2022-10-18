from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    BINARY,
)

from app.database import Base


class Firmware(Base):
    __tablename__ = "firmware"

    id = Column(Integer, primary_key=True)

    model = Column(String(128))

    hardware = Column(String(256))

    hash = Column(String(256))

    date = Column(DateTime(), default=datetime.now)

    data = Column(BINARY())
    bin = Column(BINARY())
