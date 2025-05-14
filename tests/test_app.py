from http import HTTPStatus


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


def test_create_user_should_return_created_and_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testuser',
        'email': 'test@test.com',
        'id': 1,
    }


def test_get_users_should_return_ok_and_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'testuser', 'email': 'test@test.com', 'id': 1}]
    }
    assert len(response.json()['users']) == 1


def test_update_user_should_return_ok_and_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'testuser',
            'email': 'test@test.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'testuser',
        'email': 'test@test.com',
        'id': 1,
    }


def test_delete_user_should_return_ok_and_message(client):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}
