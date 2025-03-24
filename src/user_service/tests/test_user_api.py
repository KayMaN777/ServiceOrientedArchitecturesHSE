import pytest
from unittest.mock import Mock
from user_service.api.server import UserServer

@pytest.fixture
def client():
    user_service_mock = Mock()
    app = UserServer(user_service=user_service_mock).app
    with app.test_client() as client:
        yield client, user_service_mock

def test_register(client):
    client_instance, user_service_mock = client
    user_service_mock.register.return_value = (201, {"message": "User registered"})

    response = client_instance.post('/register', json={
        'login': 'testuser',
        'password': 'password123',
        'email': 'test@example.com'
    })
    
    assert response.status_code == 201
    assert response.json == {"message": "User registered"}
    user_service_mock.register.assert_called_once_with('testuser', 'password123', 'test@example.com')

def test_login(client):
    client_instance, user_service_mock = client
    user_service_mock.login.return_value = (200, {"token": "abcd1234"})

    response = client_instance.post('/login', json={
        'login': 'testuser',
        'password': 'password123'
    })
    
    assert response.status_code == 200
    assert response.json == {"token": "abcd1234"}
    user_service_mock.login.assert_called_once_with('testuser', 'password123')

def test_update(client):
    client_instance, user_service_mock = client
    user_service_mock.update.return_value = (200, {"message": "Profile updated"})

    response = client_instance.put('/update', json={
        'firstName': 'John',
        'lastName': 'Doe',
        'birthdate': '1990-01-01',
        'email': 'john@example.com',
        'phoneNumber': '1234567890'
    }, headers={
        'Authorization': 'Bearer abcd1234'
    })
    
    assert response.status_code == 200
    assert response.json == {"message": "Profile updated"}
    user_service_mock.update.assert_called_once_with(
        'Bearer abcd1234', 'John', 'Doe', '1990-01-01', 'john@example.com', '1234567890'
    )

def test_get_profile(client):
    client_instance, user_service_mock = client
    user_service_mock.get_profile.return_value = (200, {"profile": "user_profile_data"})

    response = client_instance.get('/profile', headers={
        'Authorization': 'Bearer abcd1234'
    })
    
    assert response.status_code == 200
    assert response.json == {"profile": "user_profile_data"}
    user_service_mock.get_profile.assert_called_once_with('Bearer abcd1234')

