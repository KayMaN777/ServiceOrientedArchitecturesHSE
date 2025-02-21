from api.server import UserServer

if __name__ == '__main__':
    server = UserServer()
    server.run(host='0.0.0.0', port=5001)