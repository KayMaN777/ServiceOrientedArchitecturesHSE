import unittest
from unittest.mock import patch
import json
from flask import Flask
from api.server import ApiGatewayServer

class TestApiGatewayServer(unittest.TestCase):

    def setUp(self):
        self.user_service_host = "localhost"
        self.user_service_port = "5001"

        self.patcher = patch.dict('os.environ', {
            'USER_API_HOST': self.user_service_host,
            'USER_API_PORT': self.user_service_port,
        })
        self.patcher.start()

        self.app = ApiGatewayServer().app
        self.client = self.app.test_client()

    def tearDown(self):
        self.patcher.stop()

    @patch('requests.request')
    def test_register(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.content = b'Success'
        mock_request.return_value.headers = {'Content-Type': 'application/json'}
        
        response = self.client.post('/register', json={"login": "test", "password": "testpass"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Success')

    @patch('requests.request')
    def test_login(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.content = b'Logged in successfully'
        mock_request.return_value.headers = {'Content-Type': 'application/json'}
        
        response = self.client.post('/login', json={"login": "test", "password": "testpass"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Logged in successfully')

    @patch('requests.request')
    def test_update(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.content = b'Profile updated'
        mock_request.return_value.headers = {'Content-Type': 'application/json'}
        
        response = self.client.put('/update', json={"firstName": "John", "lastName": "Doe"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Profile updated')

    @patch('requests.request')
    def test_get_profile(self, mock_request):
        mock_request.return_value.status_code = 200
        mock_request.return_value.content = json.dumps({
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com"
        }).encode()
        mock_request.return_value.headers = {'Content-Type': 'application/json'}
        
        response = self.client.get('/profile', headers={"Authorization": "Bearer fake-token"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com"
        })

if __name__ == '__main__':
    unittest.main()
