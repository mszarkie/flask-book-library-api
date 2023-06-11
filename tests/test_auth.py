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
    print("response_data:   ", response_data)
    print("response_data['message']:   ", response_data['message'])
    print("missing_field:   ", missing_field)
    print("data:   ", data)
    #print("response_data['message'][missing_field]:   ", response_data['message'][missing_field])
    assert missing_field in response_data['message']
    assert 'Missing data for required field.' in response_data['message'][missing_field]

    db.engine.dispose()
