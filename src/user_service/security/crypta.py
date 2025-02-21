import jwt
import datetime
import bcrypt

SECRET_KEY="kayman777"

def create_jwt_token(login: str) -> str:
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'login': login, 'exp': expiration}, SECRET_KEY, algorithm='HS256')
    return token

def decode_jwt_token(token: str) -> str:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    return decoded['login']

def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(hashed: bytes, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed)
