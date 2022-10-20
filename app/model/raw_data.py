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
    """
    Model for the data that the sensor contains

    Args:

        (id): Identification field
        (upload_id):Upload id
        (sensor_id): Foreign Key on Sensor model
        (blob): blob
        (added_at): Timestamp of current model creation
        (parsed): Check if a file has been parsed

    """

    __tablename__ = "raw_datas"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    upload_id = Column(Integer, default=0)

    sensor_id = Column(Integer, ForeignKey("sensors.id"))

    blob = Column(String(256))

    added_at = Column(DateTime(), default=datetime.now)

    parsed = Column(Boolean, default=False)
