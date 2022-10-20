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
    """

    Model that stores hash for key of sensor

    Args:

       (id): Identification field
       (sensor_id): Foreign Key on Sensor model
       (group_id): Foreign Key on Group model
       (key_hash): Hash of the Key
       (created_at): Timestamp of creation current sensor's key

    """

    __tablename__ = "sensor_keys"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer, ForeignKey("sensors.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    key_hash = Column(String(256))

    created_at = Column(DateTime(), default=datetime.now)
