import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import table_registry


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


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)  # Teardown
