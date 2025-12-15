import pytest
from fastapi.testclient import TestClient

from fastapi_zero.app import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def user_alice() -> dict[str, str]:
    return {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }


@pytest.fixture
def user_bob() -> dict[str, str]:
    return {
        'username': 'bob',
        'email': 'bob@example.com',
        'password': 'secret',
    }
