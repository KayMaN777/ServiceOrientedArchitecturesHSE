from api.server import ApiGatewayServer
import os

if __name__ == '__main__':
    server = ApiGatewayServer()
    server.run(host='0.0.0.0', port=os.getenv("API_GATEWAY_PORT"))