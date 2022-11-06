from functools import lru_cache
from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.config import Settings
from app import config

Base = declarative_base()


@lru_cache
def get_engine() -> Engine:
    settings: Settings = config.get_settings()
    return create_engine(settings.DB_URI)


def get_db() -> Iterator[Session]:
    engine: Engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
