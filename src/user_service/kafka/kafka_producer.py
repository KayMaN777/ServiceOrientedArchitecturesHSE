from confluent_kafka import Producer
import json

class UserServiceKafkaProducer:
    def __init__(self, kafka_servers):
        self.producer = Producer({
            'bootstrap.servers': kafka_servers,
            'client.id': 'user_service_producer'
        })
        self.REGISTRATION_TOPIC = "registration"

    def _delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def send_registration_event(self, user_id: int, login: str, email: str):
        try:
            registrtion_message = json.dumps({
                'user_id': user_id,
                'login': login,
                'email': email
            })
            self.kafka_producer.produce(
                topic=self.REGISTRATION_TOPIC,
                key=user_id,
                value=registrtion_message,
                callback=self._delivery_report
            )
            self.kafka_producer.flush()
        except Exception as e:
            print(f'Failed to send message to Kafka: {str(e)}')