import grpc
from concurrent import futures
from api.proto.statistics_service_pb2_grpc import StatisticsServiceServicer
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from api.proto.statistics_service_pb2 import (
    ActionResponse
)

def create_timestamp(timestamp_str: str) -> Timestamp:
    dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    timestamp = Timestamp()    
    timestamp.FromDatetime(dt)
    return timestamp

class StatisticsService(StatisticsServiceServicer):
    def __init__(self, db):
        self.db = db

    def AddLike(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('post_id' not in metadata or request.post_id < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return ActionResponse()
        
        like = self.db.add_like(request.user_id, request.post_id)
        if like is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ActionResponse()
        
        like_response = ActionResponse(
            post_id=like["post_id"],
            user_id=like["user_id"],
            updated_at=create_timestamp(like["updated_at"])
        )
        return like_response
    
    def AddView(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('post_id' not in metadata or request.post_id < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return ActionResponse()
        
        view = self.db.add_view(request.user_id, request.post_id)
        if view is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return ActionResponse()
        
        view_response = ActionResponse(
            post_id=view["post_id"],
            user_id=view["user_id"],
            updated_at=create_timestamp(view["updated_at"])
        )
        return view_response