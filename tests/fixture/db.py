import pytest
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import Settings
from app.database import Base, get_db
from tests.conftest import get_test_settings


@pytest.fixture
def db() -> Generator:
    from app.main import app

    settings: Settings = get_test_settings()

    engine = create_engine(settings.DB_URI, connect_args={"check_same_thread": False})
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
