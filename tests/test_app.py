from http import HTTPStatus


def test_root_deve_retornar_ola_fastapi(client):  # Arrange
    response = client.get('/')  # Act

    assert response.json() == {'message': 'Olá FastAPI'}  # Assert
    assert response.status_code == HTTPStatus.OK  # Assert


def test_exercicio_deve_retornar_ola_mundo(client):
    response = client.get('/exercicio')

    assert 'Olá Mundo' in response.text
    assert response.status_code == HTTPStatus.OK
