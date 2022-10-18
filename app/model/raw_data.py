from datetime import datetime


from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    ForeignKey,
    DateTime,
)
from app.database import Base


class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True)

    upload_id = Column(Integer)

    sensor_id = Column(Integer, ForeignKey("sensor.id"))

    blob = Column(String(256))

    added_at = Column(DateTime(), default=datetime.now)

    parsed = Column(Boolean, default=False)
