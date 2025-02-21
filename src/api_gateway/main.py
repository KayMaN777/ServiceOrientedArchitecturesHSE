from api.server import ApiGatewayServer

if __name__ == '__main__':
    server = ApiGatewayServer()
    server.run(host='0.0.0.0', port=5000)