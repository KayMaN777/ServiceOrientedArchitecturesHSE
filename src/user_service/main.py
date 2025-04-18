from api.server import UserServer
from postgres.database import Database
from model.user_service import UserService
from security.crypta import Crypta
import os
from kafka.kafka_producer import UserServiceKafkaProducer

if __name__ == '__main__':
    crypta = Crypta()
    database = Database(crypta)
    user_service = UserService(database, crypta)
    kafka_producer = UserServiceKafkaProducer(f"{os.getenv('KAFKA_SERVER', 'kafka')}:{os.getenv('KAFKA_PORT', '9092')}")
    server = UserServer(user_service, kafka_producer)
    server.run(host='0.0.0.0', port=os.getenv("USER_API_PORT"))