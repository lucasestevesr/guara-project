import pytest
from fastapi.testclient import TestClient

from guara.app import app


@pytest.fixture
def client():
    return TestClient(app)
