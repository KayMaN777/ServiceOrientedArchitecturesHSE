import grpc
from concurrent import futures
from api.proto.statistics_service_pb2_grpc import add_StatisticsServiceServicer_to_server
from api.server import StatisticsService
import api.proto.statistics_service_pb2
from grpc_reflection.v1alpha import reflection
import os
import logging
from clickhouse.database import Database
from kafka.kafka_producer import StatisticsServiceKafkaProducer

db_params = {
    "database": os.getenv("STATISTICS_DB"),
    "user": os.getenv("STATISTICS_DB_USER"),
    "password": os.getenv("STATISTICS_DB_PASSWORD"),
    "host": os.getenv("STATISTICS_DB_HOST"),
    "port": "9000",
    "min_pool_size": "1",
    "max_pool_size": "5"
}

def serve():
    database = Database(db_params)
    kafka_producer = StatisticsServiceKafkaProducer(f"{os.getenv('KAFKA_SERVER', 'kafka')}:{os.getenv('KAFKA_PORT', '9092')}")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_StatisticsServiceServicer_to_server(StatisticsService(database, kafka_producer), server)
    SERVICE_NAMES = (
        api.proto.statistics_service_pb2.DESCRIPTOR.services_by_name['StatisticsService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    port = os.getenv("STATISTICS_API_PORT")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()