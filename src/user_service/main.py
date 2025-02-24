from api.server import UserServer
import os

if __name__ == '__main__':
    server = UserServer()
    server.run(host='0.0.0.0', port=os.getenv("USER_API_PORT"))