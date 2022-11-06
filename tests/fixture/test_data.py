import json
import pytest
from typing import Generator


@pytest.fixture
def test_data() -> Generator:
    with open("tests/test_data.json") as f:
        yield json.load(f)
