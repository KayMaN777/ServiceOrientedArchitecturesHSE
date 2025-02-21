
from flask import Flask, request, Response
import requests

class ApiGatewayServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.user_service_address = "http://localhost:5001"
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/register', methods=['POST'])
        def register():
            url = f'{self.user_service_address}/register'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
    
        @self.app.route('/login', methods=['POST'])
        def login():
            url = f'{self.user_service_address}/login'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))

        @self.app.route('/update', methods=['PUT'])
        def update():
            url = f'{self.user_service_address}/update'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
        
        @self.app.route('/profile', methods=['GET'])
        def get_profile():
            url = f'{self.user_service_address}/profile'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
        
    def run(self, host='0.0.0.0', port=5000):
        self.app.run(debug=True, host=host, port=port)

