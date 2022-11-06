import pytest
import json
from typing import Generator
from functools import lru_cache
from dotenv import dotenv_values

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.config import settings as conf
from app.config import Settings
from app import config


@lru_cache
def get_test_settings() -> Settings:
    return Settings(**dotenv_values("tests/test.env"))


@pytest.fixture
def client() -> Generator:
    if not conf.TEST_SEND_EMAIL:
        from app.controller.mail import mail

        mail.config.SUPPRESS_SEND = 1

    with TestClient(app) as c:
        yield c


@pytest.fixture
def test_data() -> Generator:
    with open("tests/test_data.json") as f:
        yield json.load(f)


@pytest.fixture
def db() -> Generator:
    # SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:

        def override_get_db() -> Generator:
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        yield db


pytest_plugins = [
    "tests.fixture.gateway_channel",
]

config.get_settings = get_test_settings
