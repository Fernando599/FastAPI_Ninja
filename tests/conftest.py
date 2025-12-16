import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fastapi_zero.app import app
from fastapi_zero.database import get_session
from fastapi_zero.models import table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)  # Teardown


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
