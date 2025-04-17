import grpc
from concurrent import futures
from api.proto.content_service_pb2_grpc import ContentServiceServicer
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime
from api.proto.content_service_pb2 import (
    Post, DeletePostResponse, PostsList, Comment, CommentsList
)

def create_timestamp(current_time):
    timestamp = Timestamp()
    timestamp.FromDatetime(current_time)
    return timestamp

class ContentService(ContentServiceServicer):
    def __init__(self, db):
        self.db = db

    def AddPost(self, request, context):
        metadata = dict(context.invocation_metadata())
        tags = list(request.tags) if 'tags' in metadata else None
        is_private = request.is_private if 'is_private' in metadata else False
        for required_field in ['user_id', 'title', 'description']:
            if required_field not in metadata:
                context.set_details('Invalid arguments')
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                return Post()

        added_post = self.db.add_post(request.user_id, request.title, request.description, tags, is_private)
        if added_post is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return Post()
        
        added_post["created_at"] = create_timestamp(added_post["created_at"])
        added_post["updated_at"] = added_post["created_at"]
        return Post(**added_post)
    
    def DeletePost(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('post_id' not in metadata or request.post_id < 0) or
            ('user_id' not in metadata or request.user_id < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return DeletePostResponse()

        status = self.db.delete_post(request.post_id, request.user_id)
        if status is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return DeletePostResponse()
        
        response = DeletePostResponse(success=status)
        return response

    def UpdatePost(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('post_id' not in metadata or request.post_id < 0) or
            ('user_id' not in metadata or request.user_id < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Post()
        
        title = request.title if 'title' in metadata else None
        description = request.description if 'description' in metadata else None
        is_private = request.is_private if 'is_private' in metadata else None
        tags = list(request.tags) if 'tags' in metadata else None

        updated_post = self.db.update_post(request.post_id, request.user_id, title, description, is_private, tags)
        if updated_post is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return Post()
        
        updated_post["updated_at"] = create_timestamp(updated_post["updated_at"])
        return Post(**updated_post)

    def GetPostById(self, request, context):
        metadata = dict(context.invocation_metadata())
        if 'post_id' not in metadata or request.post_id < 0:
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Post()
        
        post = self.db.get_post(request.post_id)
        if post is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return Post()
        
        post["created_at"] = create_timestamp(post["created_at"])
        post["updated_at"] = create_timestamp(post["updated_at"])
        print(post)
        return Post(**post)

    def GetUserPosts(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('limit' not in metadata or request.limit < 0) or
            ('offset' not in metadata or request.offset < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return PostsList()

        posts = self.db.get_user_posts(request.user_id, request.limit, request.offset)
        if posts is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return PostsList()
        
        for post in posts:
            post["created_at"] = create_timestamp(post["created_at"])
            post["updated_at"] = create_timestamp(post["updated_at"])

        return PostsList(posts=posts)

    def GetAllPosts(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('limit' not in metadata or request.limit < 0) or
            ('offset' not in metadata or request.offset < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return PostsList()
    
        posts = self.db.get_posts(request.user_id, request.limit, request.offset)
        if posts is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return PostsList()
        
        for post in posts:
            post["created_at"] = create_timestamp(post["created_at"])
            post["updated_at"] = create_timestamp(post["updated_at"])

        return PostsList(posts=posts)
    
    def AddComment(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('post_id' not in metadata or request.post_id < 0) or 'description' not in metadata):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return Comment()
        
        comment = self.db.add_comment(request.user_id, request.post_id, request.description)
        if comment is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return Comment()
        
        comment_response = Comment(
            post_id=comment["post_id"],
            user_id=comment["user_id"],
            created_at=create_timestamp(comment["created_at"]),
            updated_at=create_timestamp(comment["updated_at"]),
            description=comment["description"]
        )
        return comment_response
    
    def GetComments(self, request, context):
        metadata = dict(context.invocation_metadata())
        if (('user_id' not in metadata or request.user_id < 0) or
            ('post_id' not in metadata or request.post_id < 0) or
            ('limit' not in metadata or request.limit < 0) or 
            ('offset' not in metadata or request.offset < 0)):
            context.set_details('Invalid arguments')
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return CommentsList()

        comments = self.db.get_comments(request.post_id, request.user_id, request.limit, request.offset)
        if comments is None:
            context.set_details('Internal error')
            context.set_code(grpc.StatusCode.INTERNAL)
            return CommentsList()
        
        for comment in comments:
            comment["created_at"] = create_timestamp(comment["created_at"])
            comment["updated_at"] = create_timestamp(comment["updated_at"])

        return CommentsList(comments=comments)