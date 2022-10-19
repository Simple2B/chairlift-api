from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from app.database import Base


class SensorKey(Base):
    __tablename__ = "sensor_keys"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    key_hash = Column(String(256))

    created_at = Column(DateTime(), default=datetime.now)
