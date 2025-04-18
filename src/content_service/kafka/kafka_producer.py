from confluent_kafka import Producer
import json

class ContentServiceKafkaProducer:
    def __init__(self, kafka_servers):
        self.producer = Producer({
            'bootstrap.servers': kafka_servers,
            'client.id': 'content_service_producer'
        })
        self.COMMENTS_TOPIC = "comment"

    def _delivery_report(self, err, msg):
        """Called once for each message produced to indicate delivery result."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
    def send_comment_event(self, post_id: int, user_id: int, created_at: str, updated_at: str):
        try:
            message = json.dumps({
                'post_id': post_id,
                'user_id': user_id,
                'created_at': created_at,
                'updated_at': updated_at
            })
            self.kafka_producer.produce(
                topic=self.COMMENTS_TOPIC,
                key=post_id,
                value=message,
                callback=self._delivery_report
            )
            self.kafka_producer.flush()
        except Exception as e:
            print(f'Failed to send message to Kafka: {str(e)}')
