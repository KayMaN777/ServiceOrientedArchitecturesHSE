import re

class UserService:
    def __init__(self, database, crypta):
        self.database = database
        self.crypta = crypta
    
    @staticmethod
    def validate_email(email: str) -> bool:
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return re.match(email_regex, email)
    
    @staticmethod
    def validate_phone_number(phone_number: str) -> bool:
        phone_regex = re.compile(
            r"^\+\d{8,15}$"
        )
        return re.match(phone_regex, phone_number)
    
    @staticmethod
    def validate_birth_date(birth_date: str) -> bool:
        pattern = r"^(?:(?:19|20)\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$"
        return re.match(pattern, birth_date) is not None

    def register(self, login: str, password: str, email: str) -> tuple[int, dict]:
        if login is None:
            return 400, {"message": "Field login must be filled"}
        if password is None:
            return 400, {"message": "Field password must be filled"}
        if not UserService.validate_email(email):
            return 400, {"message": "Invalid email"}
        status, response = self.database.register(login, self.crypta.hash_password(password), email)
        return status, response

    def login(self, login: str, password: str) -> tuple[int, dict]:
        if not login or not password:
            return 400, {"message": "Login and Password must be filled in"}
        status, response = self.database.login(login, password)
        return status, response
    
    def update(self, token, first_name: str, last_name: str, birth_date: str, email: str, phone_number: str) -> tuple[int, dict]:
        if (email is not None and not UserService.validate_email(email)):
            return 400, {"message": "Incorrect email"}
        if (phone_number is not None and not UserService.validate_phone_number(phone_number)):
            return 400, {"message": "Incorrect phone number"}
        if (birth_date is not None and not UserService.validate_birth_date(birth_date)):
            return 400, {"message": "Incorrect birthdate"}
        status, response = self.database.update(token, first_name, last_name, birth_date, email, phone_number)
        return status, response
    
    def get_profile(self, token: str) -> tuple[int, dict]:
        status, response = self.database.get_profile(token)
        return status, response
    
    def get_user_id(self, login):
        response = self.database.get_user_id(login)
        return response
