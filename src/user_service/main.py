from api.server import UserServer
from postgres.database import Database
from model.user_service import UserService
from security.crypta import Crypta
import os

if __name__ == '__main__':
    crypta = Crypta()
    database = Database(crypta)
    user_service = UserService(database, crypta)
    server = UserServer(user_service)
    server.run(host='0.0.0.0', port=os.getenv("USER_API_PORT"))