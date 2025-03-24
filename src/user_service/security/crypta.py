import jwt
import datetime
import bcrypt
import os

class Crypta:
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY")

    def create_jwt_token(self, login: str) -> str:
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        token = jwt.encode({'login': login, 'exp': expiration}, self.secret_key, algorithm='HS256')
        return token

    def decode_jwt_token(self, token: str) -> str:
        decoded = jwt.decode(token, self.secret_key, algorithms=['HS256'])
        return decoded['login']

    def hash_password(self, password: str) -> bytes:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def check_password(self, hashed: bytes, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
