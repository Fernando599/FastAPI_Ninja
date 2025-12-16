from http import HTTPStatus


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


def test_user_already_exists(client, user_alice):
    response_1 = client.post('/users/', json=user_alice)
    assert response_1.status_code == HTTPStatus.CREATED

    response_2 = client.post('/users/', json=user_alice)

    assert response_2.status_code == HTTPStatus.CONFLICT
    assert response_2.json() == {'detail': 'Username already exists'}


def test_email_already_exists(client, user_bob):
    client.post('/users/', json=user_bob)

    user_with_same_email = {
        'username': 'outronome',
        'email': 'bob@example.com',
        'password': 'secret',
    }

    response_2 = client.post('/users/', json=user_with_same_email)

    assert response_2.status_code == HTTPStatus.CONFLICT
    assert response_2.json() == {'detail': 'Email already exists'}


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


def test_update_user_with_same_username(client, user_alice, user_bob):
    client.post('/users/', json=user_alice)
    client.post('/users/', json=user_bob)

    user_with_same_username = {
        'username': 'alice',
        'email': 'outroemail@gmail.com',
        'password': 'secret',
    }

    response = client.put('/users/2', json=user_with_same_username)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_update_user_with_same_email(client, user_alice, user_bob):
    client.post('/users/', json=user_alice)
    client.post('/users/', json=user_bob)

    user_with_same_email = {
        'username': 'outronome',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.put('/users/2', json=user_with_same_email)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


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
    assert response.json() == {'message': 'User deleted'}


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


def test_get_one_user_invalid_id(client):
    response = client.get('/users/-1')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
