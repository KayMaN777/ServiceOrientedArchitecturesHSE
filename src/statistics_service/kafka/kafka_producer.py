from confluent_kafka import Producer
import json

class StatisticsServiceKafkaProducer:
    def __init__(self, kafka_servers):
        self.producer = Producer({
            'bootstrap.servers': kafka_servers,
            'client.id': 'statistics_service_producer'
        })
        self.LIKES_TOPIC = "likes"
        self.VIEWS_TOPIC = "views"

    def _delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def send_like_event(self, post_id: int, user_id: int, timestamp: str):
        try:
            message = json.dumps({
                'post_id': post_id,
                'user_id': user_id,
                'timestamp': timestamp
            })
            self.kafka_producer.produce(
                topic=self.LIKES_TOPIC,
                key=post_id,
                value=message,
                callback=self._delivery_report
            )
            self.kafka_producer.flush()
        except Exception as e:
            print(f'Failed to send message to Kafka: {str(e)}')
    
    def send_view_event(self, post_id: int, user_id: int, timestamp: str):
        try:
            message = json.dumps({
                'post_id': post_id,
                'user_id': user_id,
                'timestamp': timestamp
            })
            self.kafka_producer.produce(
                topic=self.VIEWS_TOPIC,
                key=post_id,
                value=message,
                callback=self._delivery_report
            )
            self.kafka_producer.flush()
        except Exception as e:
            print(f'Failed to send message to Kafka: {str(e)}')
