from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
    Float,
    DateTime,
    ForeignKey,
    LargeBinary,
)

from app.database import Base


class Sensor(Base):
    """Model that describes sensors

    Args:

       (id): Identification field
       (upload_id): Id of upload
       (sensor_name): Name of the sensor
       (sensor_location_x): Sensor`s location on x axis
       (sensor_location_y): Sensor`s location on y axiss
       (config): Sensor`s config data
       (health): Sensor`s health data
       (is_public): Checks if current sensor is public
       (created_at): Timestamp of creation date of current sensor

    """

    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)
    upload_id = Column(Integer)
    sensor_name = Column(String(128), index=True)

    sensor_location_x = Column(Float)
    sensor_location_y = Column(Float)

    config = Column(String(256))
    health = Column(String(256))

    is_public = Column(Boolean, default=False)

    created_at = Column(DateTime(), default=datetime.now)


class SensorData(Base):
    __tablename__ = "sensor_datas"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)

    data_id = Column(Integer, ForeignKey("raw_datas.id"))

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

    health = Column(LargeBinary)
