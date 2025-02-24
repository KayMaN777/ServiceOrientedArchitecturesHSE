from datetime import datetime, timedelta
from security.crypta import create_jwt_token, decode_jwt_token, check_password
import jwt
import psycopg2
from psycopg2 import sql
from psycopg2 import pool

db_params = {
    "database": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

class Database:
    def __init__(self):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,             
            maxconn=10,             
            **db_params
        )
        self.users_db = {}
    
    def execute_query(self, query:str, params = None) -> tuple[bool, list]:
        connection = None
        result = None
        status = True
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(query, params)

            if (query.strip().upper().startswith("SELECT")):
                result = cursor.fetchall()
            else:
                connection.commit()
        except Exception as error:
            print(f"Error while query: {error}")
            status = False
        finally:
            if connection:
                cursor.close()
                self.connection_pool.putconn(connection)
        return status, result

    def get_user_id(self, login: str) -> str:
        query = """SELECT * from Users WHERE username = %s"""
        params = (login,)
        status, result = self.execute_query(query, params)
        if status:
            result = result[0][0]
        return result

    def add_token(self, login: str) -> tuple[bool, str]:
        user_id = self.get_user_id(login)
        if user_id is None:
            return False, None
        token = create_jwt_token(login)
        query = """INSERT INTO Sessions (userId, token, expiresAt) VALUES (%s, %s, %s)"""
        params = (user_id, token, datetime.now() + timedelta(hours = 1))
        status, _ = self.execute_query(query, params)
        if not status:
            return False, None
        return True, token
    
    def check_session(self, login: str, token: str) -> list:
        user_id = self.get_user_id(login)
        if user_id is None:
            return False
        query = """SELECT * FROM Sessions WHERE userId = %s AND token = %s"""
        params = (user_id, token)
        status, result = self.execute_query(query, params)
        if not status or not result:
            return False
        return True

    def register_transaction(self, login: str, password_hash: bytes, email: str) -> tuple[bool, str]:
        connection = None
        status = True
        token = None
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO Users (username, email, passwordHash) VALUES (%s, %s, %s)""",
                           (login, email, password_hash))
            cursor.execute("""SELECT userId FROM Users WHERE username = %s""",
                           (login,))
            user_id = cursor.fetchall()[0][0]
            cursor.execute("""INSERT INTO Profiles (userId, email) VALUES (%s, %s)""",
                           (user_id, email))
            token = create_jwt_token(login)
            cursor.execute("""INSERT INTO Sessions (userId, token, expiresAt) VALUES (%s, %s, %s)""",
                           (user_id, token, datetime.now() + timedelta(hours = 1)))
            connection.commit()
        except Exception as error:
            print(f"Error while query: {error}")
            status = False
        finally:
            if connection:
                cursor.close()
                self.connection_pool.putconn(connection)
        return status, token

    def register(self, login: str, password_hash: bytes, email: str) -> tuple[int, dict]:
        query = """SELECT * from Users WHERE username = %s OR email = %s"""
        params = (login, email)
        status, result = self.execute_query(query, params)
        if not status:
            return 404, {"message": "Internal error"}
        if result:
            return 409, {"message": "Username or email allready exists"}
        
        status, token = self.register_transaction(login, password_hash, email)
        if not status:
            return 404, {"message": "Internal error"}
        
        return 200, {"token": token}

    def login(self, login: str, password: str) -> tuple[int, dict]:
        query = """SELECT * FROM Users WHERE username = %s"""
        params = (login,)
        status, result = self.execute_query(query, params)
        if not status:
            return 404, {"message": "Internal error"}
        if not result or not check_password(bytes(result[0][3]), password):
            return 401, {"message": "Invalid username or password"}
        status, token = self.add_token(login)
        if not status:
            return 404, {"message": "Internal error"}
        return 200, {"token": token}

    def validate_token(self, token: str) -> tuple[int, dict]:
        try:
            login = decode_jwt_token(token)
            if not self.check_session(login, token):
                return 404, {"message": "No such session"}
            return 200, login
        except jwt.ExpiredSignatureError:
            return 401, {"message": "Authentification token allready expired"}
        except jwt.InvalidTokenError:
            return 401, {"message": "Incorrect authentification token"}
        
    def add_field(self, params:list, fields:list, field_name:str, field_param:str) -> None:
        if field_param:
            fields.append(field_name)
            params.append(field_param)

    def update(self, token, first_name: str, last_name: str, birth_date: str, email: str, phone_number: str) -> tuple[int, dict]:
        status, response = self.validate_token(token)
        if (status != 200):
            return status, response
        user_id = self.get_user_id(response)
        if user_id is None:
            return 404, {"message": "Internal error"}
        query = """UPDATE Profiles SET """
        params = []
        fields = []
        for field_name, field_param in zip(["firstName = %s", "lastName = %s", "birthdate = %s", "email = %s", "phoneNumber = %s"],
                                           [first_name, last_name, birth_date, email, phone_number]):
            self.add_field(params, fields, field_name, field_param)
        print(fields)
        print(params)
        if not params:
            return 200, {"message": "Profile successfully updated"}
        query += ", ".join(fields)
        query += " WHERE userId = %s;"
        params.append(user_id)
        params = tuple(params)
        status, _ = self.execute_query(query, params)
        if not status:
            return 404, {"message": "Internal error"}
        return 200, {"message": "Profile successfully updated"}

    def get_profile(self, token: str) -> tuple[int, dict]:
        status, response = self.validate_token(token)
        if (status != 200):
            return status, response
        user_id = self.get_user_id(response)
        if user_id is None:
            return 404, {"message": "Internal error"}
        query = """SELECT * FROM Profiles WHERE userId = %s"""
        params = (user_id,)
        status, response = self.execute_query(query, params)
        if not status:
            return 404, {"message": "Internal error"}
        print(response)
        response_data = {"firstName": response[0][1],
                         "lastName": response[0][2],
                         "birthdate": response[0][3].strftime("%Y-%m-%d"),
                         "email": response[0][4],
                         "phoneNumber": response[0][5]}
        return 200, response_data
