from http import HTTPStatus

from fastapi_zero.app import database


def test_root_deve_retornar_ola_fastapi(client):  # Arrange
    response = client.get('/')  # Act

    assert response.json() == {'message': 'Olá FastAPI'}  # Assert
    assert response.status_code == HTTPStatus.OK  # Assert


def test_exercicio_deve_retornar_ola_mundo(client):
    response = client.get('/exercicio')

    assert 'Olá Mundo' in response.text
    assert response.status_code == HTTPStatus.OK


def test_create_user(client, user_alice):
    response = client.post('/users/', json=user_alice)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }
    database.clear()


def test_list_users(client, user_alice, user_bob):
    client.post('/users/', json=user_alice)
    client.post('/users/', json=user_bob)

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'username': 'alice', 'email': 'alice@example.com', 'id': 1},
            {'username': 'bob', 'email': 'bob@example.com', 'id': 2},
        ],
    }

    database.clear()


def test_update_user(client, user_alice):
    client.post('/users/', json=user_alice)

    response = client.put(
        '/users/1',
        json={
            'username': 'alice alterado',
            'email': 'alice_alterado@example.com',
            'password': 'secretAlterado',
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice alterado',
        'email': 'alice_alterado@example.com',
        'id': 1,
    }

    database.clear()


def test_update_user_invalid_id(client):
    response = client.put(
        '/users/-1',
        json={
            'username': 'ghost',
            'email': 'ghost@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user(client, user_alice):
    client.post('/users/', json=user_alice)

    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }

    database.clear()


def test_delete_user_invalid_id(client):
    response = client.delete('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_get_one_user_in_list(client, user_alice, user_bob):
    client.post('/users/', json=user_alice)
    client.post('/users/', json=user_bob)

    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }

    database.clear()


def test_get_one_user_invalid_id(client):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
