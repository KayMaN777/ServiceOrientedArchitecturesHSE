from security.crypta import create_jwt_token, decode_jwt_token, check_password
import jwt

class Database:
    def __init__(self):
        self.users_db = {}
    
    def register(self, login: str, password_hash: bytes, email: str) -> tuple[int, dict]:
        if login in self.users_db:
            return 409, {"message": "Username or email already exists"}
        self.users_db[login] = {'password_hash': password_hash, 'email': email}
        return 200, {"token": create_jwt_token(login)}

    def login(self, login: str, password: str) -> tuple[int, dict]:
        user = self.users_db.get(login)
        if not user or not check_password(user['password_hash'], password):
            return 401, {"message": "Invalid username or password"}
        return 200, {"token": create_jwt_token(login)}

    def validate_token(self, token: str) -> tuple[int, dict]:
        try:
            login = decode_jwt_token(token)
            user = self.users_db.get(login)
            if not user:
                return 404, {"message": "No such user"}
            return 200, login
        except jwt.ExpiredSignatureError:
            return 401, {"message": "Authentification token allready expired"}
        except jwt.InvalidTokenError:
            return 401, {"message": "Incorrect authentification token"}
        
    def update(self, token, first_name: str, last_name: str, birth_date: str, email: str, phone_number: str) -> tuple[int, dict]:
        status, response = self.validate_token(token)
        if (status != 200):
            return status, response
        if first_name:
            self.users_db[response]["first_name"] = first_name
        if last_name:
            self.users_db[response]["last_name"] = last_name
        if birth_date:
            self.users_db[response]["birth_date"] = birth_date
        if email:
            self.users_db[response][email] = email
        if phone_number:
            self.users_db[response]["phone_number"] = phone_number 
        return 200, {"message": "Profile successfully updated"}
    
    def get_profile(self, token: str) -> tuple[int, dict]:
        status, response = self.validate_token(token)
        if (status != 200):
            return status, response
        first_name = self.users_db[response].get("first_name", "")
        last_name = self.users_db[response].get("last_name", "")
        birth_date = self.users_db[response].get("birth_date", "")
        email = self.users_db[response].get("email", "")
        phone_number = self.users_db[response].get("phone_number", "")
        response_data = {"firstName": first_name,
                         "lastName": last_name,
                         "dateOfBirth": birth_date,
                         "email": email,
                         "phoneNumber": phone_number}
        return 200, response_data
