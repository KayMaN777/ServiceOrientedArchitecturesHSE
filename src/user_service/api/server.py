
from flask import Flask, request, Response
import json
from model.user_service import UserService

class UserServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.user_service = UserService()
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/register', methods=['POST'])
        def register():
            data = request.json
            login = data.get('login')
            password = data.get('password')
            email = data.get('email')
            status, response = self.user_service.register(login, password, email)
            return self.create_response(response, status)

        @self.app.route('/login', methods=['POST'])
        def login():
            data = request.json
            login = data.get('login')
            password = data.get('password')
            status, response = self.user_service.login(login, password)
            return self.create_response(response, status)
                
        @self.app.route('/update', methods = ['PUT'])
        def update():
            token = request.headers.get('Authorization')
            data = request.json
            first_name = data.get("firstName")
            last_name = data.get("lastName")
            birth_date = data.get("birthdate")
            email = data.get("email")
            phone_number = data.get("phoneNumber")
            status, response = self.user_service.update(token, first_name, last_name, birth_date, email, phone_number)
            return self.create_response(response, status)
                
        @self.app.route('/profile', methods = ['GET'])
        def get_profile():
            token = request.headers.get('Authorization')
            status, response = self.user_service.get_profile(token)
            return self.create_response(response, status)

    def create_response(self, data, status):
        response_json = json.dumps(data, ensure_ascii=False)
        return Response(response_json, status=status, content_type='application/json; charset=utf-8')

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(debug=True, host=host, port=port)


