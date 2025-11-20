from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app


def test_root_deve_retornar_ola_fastapi():
    client = TestClient(app) # Arrange

    response = client.get('/') # Act

    assert response.json() == {'message': 'Olá FastAPI'} # Assert
    assert response.status_code == HTTPStatus.OK # Assert