import pytest
from unittest.mock import Mock
from user_service.model.user_service import UserService

@pytest.fixture
def mock_database():
    return Mock()

@pytest.fixture
def mock_crypta():
    crypta = Mock()
    crypta.hash_password = Mock(return_value='hashed_password')
    return crypta

@pytest.fixture
def user_service(mock_database, mock_crypta):
    return UserService(database=mock_database, crypta=mock_crypta)

def test_register_success(user_service, mock_database, mock_crypta):
    mock_database.register.return_value = (201, {"message": "User registered"})

    status, response = user_service.register('testuser', 'password123', 'test@example.com')
    
    assert status == 201
    assert response == {"message": "User registered"}
    mock_crypta.hash_password.assert_called_once_with('password123')
    mock_database.register.assert_called_once_with('testuser', 'hashed_password', 'test@example.com')

def test_register_invalid_email(user_service):
    status, response = user_service.register('testuser', 'password123', 'invalid-email')
    
    assert status == 400
    assert response == {"message": "Invalid email"}

def test_login_success(user_service, mock_database):
    mock_database.login.return_value = (200, {"token": "abcd1234"})

    status, response = user_service.login('testuser', 'password123')
    
    assert status == 200
    assert response == {"token": "abcd1234"}
    mock_database.login.assert_called_once_with('testuser', 'password123')

def test_login_missing_fields(user_service):
    status, response = user_service.login('', '')
    
    assert status == 400
    assert response == {"message": "Login and Password must be filled in"}

def test_update_valid_data(user_service, mock_database):
    mock_database.update.return_value = (200, {"message": "Profile updated"})

    status, response = user_service.update('token', 'John', 'Doe', '1990-01-01', 'john@example.com', '+1234567890')
    
    assert status == 200
    assert response == {"message": "Profile updated"}
    mock_database.update.assert_called_once_with('token', 'John', 'Doe', '1990-01-01', 'john@example.com', '+1234567890')

def test_update_invalid_email(user_service):
    status, response = user_service.update('token', 'John', 'Doe', '1990-01-01', 'invalid-email', '+1234567890')
    
    assert status == 400
    assert response == {"message": "Incorrect email"}

def test_update_invalid_phone(user_service):
    status, response = user_service.update('token', 'John', 'Doe', '1990-01-01', 'john@example.com', 'invalid-phone')
    
    assert status == 400
    assert response == {"message": "Incorrect phone number"}

def test_update_invalid_birthdate(user_service):
    status, response = user_service.update('token', 'John', 'Doe', 'invalid-date', 'john@example.com', '+1234567890')
    
    assert status == 400
    assert response == {"message": "Incorrect birthdate"}

def test_get_profile_success(user_service, mock_database):
    mock_database.get_profile.return_value = (200, {"profile": "user_profile_data"})

    status, response = user_service.get_profile('token')
    
    assert status == 200
    assert response == {"profile": "user_profile_data"}
    mock_database.get_profile.assert_called_once_with('token')
