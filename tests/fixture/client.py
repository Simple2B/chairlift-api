import pytest
from fastapi.testclient import TestClient
from typing import Generator


@pytest.fixture
def client() -> Generator:
    from app.main import app

    with TestClient(app) as c:
        yield c
