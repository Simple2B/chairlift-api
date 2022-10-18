import datetime
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    Float,
    DateTime,
    ForeignKey,
    BINARY,
)

from app.database import Base


class Sensor(Base):
    __tablename__ = "sensor"

    id = Column(Integer, primary_key=True)
    upload_id = Column(Integer)
    sensor_name = Column(String(128), index=True)

    sensor_location_x = Column(Float)
    sensor_location_y = Column(Float)

    config = Column(String(256))
    health = Column(String(256))

    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(), default=datetime.now)


class SensorKey(Base):
    __tablename__ = "sensor_key"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer, ForeignKey("sensor.id"))
    group_id = Column(Integer, ForeignKey("group.id"))

    key_hash = Column(String(256))

    created_at = Column(DateTime(), default=datetime.now)


class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)

    data_id = Column(Integer, ForeignKey("raw_data.id"))

    sensor_id = Column(String(256))

    timestamp = Column(DateTime(), default=datetime.now)

    power_current = Column(Float(precision=3))
    power_voltage = Column(Float(precision=3))
    tmp_temp = Column(Float(precision=3))
    snodar_distance = Column(Float(precision=3))
    seosonal_snowfall = Column(Float(precision=3))
    seosonal_snowdepth = Column(Float(precision=3))
    new_snowfall = Column(Float(precision=3))
    doy_swe = Column(Float(precision=3))
    temp_swe = Column(Float(precision=3))

    health = Column(BINARY)
