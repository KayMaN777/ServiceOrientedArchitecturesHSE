import grpc
from concurrent import futures
from api.proto.content_service_pb2_grpc import add_ContentServiceServicer_to_server
from api.server import ContentService
import api.proto.content_service_pb2
from grpc_reflection.v1alpha import reflection
import os
import logging
from postgres.database import Database

db_params = {
    "database": os.getenv("CONTENT_DB"),
    "user": os.getenv("CONTENT_DB_USER"),
    "password": os.getenv("CONTENT_DB_PASSWORD"),
    "host": os.getenv("CONTENT_DB_HOST"),
    "port": "5432"
}

def serve():
    database = Database(db_params)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_ContentServiceServicer_to_server(ContentService(database), server)
    SERVICE_NAMES = (
        api.proto.content_service_pb2.DESCRIPTOR.services_by_name['ContentService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    port = os.getenv("CONTENT_API_PORT")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    # print("I AM HERE CONTENT SERVICE")
    serve()