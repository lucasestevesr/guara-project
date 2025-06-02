from http import HTTPStatus


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
    client, user):
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


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_update_integrity_error(client, user):
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


def test_update_user_should_return_not_found(client):
    response = client.put(
        '/users/999',
        json={
            'username': 'non_existent_user',
            'email': 'not_found@gmail.com',
            'password': 'not_found_password',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'User deleted successfully',
    }


def test_delete_user_should_return_not_found(client):
    response = client.delete('/users/999')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


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
