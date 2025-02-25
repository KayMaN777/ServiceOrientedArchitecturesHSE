import pytest
from unittest.mock import patch
import jwt
import bcrypt
import os
from user_service.security.crypta import Crypta

@pytest.fixture
def crypta():
    with patch.dict(os.environ, {"SECRET_KEY": "test_secret"}):
        return Crypta()

def test_create_jwt_token(crypta):
    login = "testuser"
    token = crypta.create_jwt_token(login)
    assert token is not None
    
    decoded = jwt.decode(token, "test_secret", algorithms=['HS256'])
    assert decoded['login'] == login
    assert 'exp' in decoded

def test_decode_jwt_token(crypta):
    login = "testuser"
    token = crypta.create_jwt_token(login)
    
    decoded_login = crypta.decode_jwt_token(token)
    assert decoded_login == login

def test_hash_password(crypta):
    password = "securepassword"
    hashed = crypta.hash_password(password)

    assert hashed != password.encode('utf-8')
    assert bcrypt.checkpw(password.encode('utf-8'), hashed)

def test_check_password(crypta):
    password = "securepassword"
    hashed = crypta.hash_password(password)
    
    assert crypta.check_password(hashed, password) is True
    assert crypta.check_password(hashed, "wrongpassword") is False
