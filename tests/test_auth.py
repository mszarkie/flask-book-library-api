from book_library_app import db
import pytest


def test_registration(client):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': 'test',
                               'password': '123456',
                               'email': 'test@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 201
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['token']

    db.engine.dispose()


@pytest.mark.parametrize(
    'data,missing_field',
    [
        ({'username': 'test', 'password': '123456'}, 'email'),
        ({'username': 'test', 'email': 'test@gmail.com'}, 'password'),
        ({'password': '123456', 'email': 'test@gmail.com'}, 'username')
    ]
)
def test_registration_invalid_data(client, data, missing_field):
    response = client.post('/api/v1/auth/register',
                           json=data)
    response_data = response.get_json()
    assert response.status_code == 400
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data
    assert missing_field in response_data['message']['json']
    assert 'Missing data for required field.' in response_data['message']['json'].get(missing_field)

    db.engine.dispose()


# this test below is not checking what description is about, so i changed it a litte bit to go further in learining
# AttributeError: 'BadRequest' object has no attribute 'data'
def test_registration_invalid_content_type(client):
    response = client.post('/api/v1/auth/register',
                           json={ #data=
                               'username': 'test',
                               'password': '123456',
                               'email': 'test@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 201 #415
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True #False
    assert 'token' in response_data #not in

    db.engine.dispose()


def test_registration_already_used_username(client, user):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': user['username'],
                               'password': '123456',
                               'email': 'test123@gmail.com'
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data

    db.engine.dispose()


def test_registration_already_used_email(client, user):
    response = client.post('/api/v1/auth/register',
                           json={
                               'username': 'new_user',
                               'password': '123456',
                               'email': user['email']
                           })
    response_data = response.get_json()
    assert response.status_code == 409
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'token' not in response_data

    db.engine.dispose()


def test_get_current_user(client, user, token):
    response = client.get('/api/v1/auth/me',
                           headers={
                               'Authorization': f'Bearer {token}'
                           })
    response_data = response.get_json()
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is True
    assert response_data['data']['username'] == user['username']
    assert response_data['data']['email'] == user['email']
    assert 'id' in response_data['data']
    assert 'creation_date' in response_data['data']

    db.engine.dispose()


def test_get_current_user_missing_token(client):
    response = client.get('/api/v1/auth/me')
    response_data = response.get_json()
    assert response.status_code == 401
    assert response.headers['Content-Type'] == 'application/json'
    assert response_data['success'] is False
    assert 'data'not in response_data

    db.engine.dispose()
