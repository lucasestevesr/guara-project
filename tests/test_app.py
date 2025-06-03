from http import HTTPStatus

from guara.security import create_access_token


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'Geddel_vieira_lima',
            'email': 'gddel@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'Geddel_vieira_lima',
        'email': 'gddel@gmail.com',
        'id': 1,
    }


def test_create_user_should_return_409_email_unique_constraint(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'test_user',
            'email': 'Gdel@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Email already exists'}


def test_create_user_should_return_409_username_unique_constraint(
    client, user
):
    response = client.post(
        '/users/',
        json={
            'username': 'Gdel',
            'email': 'test_email@gmail.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username already exists'}


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'Gdel',
        'email': 'Gdel@gmail.com',
        'id': 1,
    }


def test_get_user_should_return_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'gdel_updated',
            'email': 'gdel_updated@gmail.com',
            'password': 'new_secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'gdel_updated',
        'email': 'gdel_updated@gmail.com',
        'id': user.id,
    }


def test_update_integrity_error(client, user, token):
    client.post(
        '/users',
        json={
            'username': 'gdel_vieira_lima',
            'email': 'gdelvieira@gmail.com',
            'password': 'secret',
        },
    )

    # changing fixture user to have the same username and email
    response_update = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'gdel_vieira_lima',
            'email': 'gdelvieira@gmail.com',
            'password': 'secret',
        },
    )
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists',
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted successfully',
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={
            'username': user.email,
            'password': user.clean_password,
        },
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_current_user_not_found(client):
    data = {'no-email': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_not_exists(client):
    data = {'sub': 'test@test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_root_should_return_ok_and_hello_world(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_root_html_should_ok_and_html_response(client):
    response = client.get('/html')
    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """
    )
