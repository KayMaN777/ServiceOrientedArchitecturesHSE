# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import api.proto.content_service_pb2 as content__service__pb2

GRPC_GENERATED_VERSION = '1.71.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in content_service_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class ContentServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AddPost = channel.unary_unary(
                '/ContentService/AddPost',
                request_serializer=content__service__pb2.AddPostRequest.SerializeToString,
                response_deserializer=content__service__pb2.Post.FromString,
                _registered_method=True)
        self.DeletePost = channel.unary_unary(
                '/ContentService/DeletePost',
                request_serializer=content__service__pb2.DeletePostRequest.SerializeToString,
                response_deserializer=content__service__pb2.DeletePostResponse.FromString,
                _registered_method=True)
        self.UpdatePost = channel.unary_unary(
                '/ContentService/UpdatePost',
                request_serializer=content__service__pb2.UpdatePostRequest.SerializeToString,
                response_deserializer=content__service__pb2.Post.FromString,
                _registered_method=True)
        self.GetPostById = channel.unary_unary(
                '/ContentService/GetPostById',
                request_serializer=content__service__pb2.GetPostByIdRequest.SerializeToString,
                response_deserializer=content__service__pb2.Post.FromString,
                _registered_method=True)
        self.GetUserPosts = channel.unary_unary(
                '/ContentService/GetUserPosts',
                request_serializer=content__service__pb2.GetPostsRequest.SerializeToString,
                response_deserializer=content__service__pb2.PostsList.FromString,
                _registered_method=True)
        self.GetAllPosts = channel.unary_unary(
                '/ContentService/GetAllPosts',
                request_serializer=content__service__pb2.GetPostsRequest.SerializeToString,
                response_deserializer=content__service__pb2.PostsList.FromString,
                _registered_method=True)
        self.AddComment = channel.unary_unary(
                '/ContentService/AddComment',
                request_serializer=content__service__pb2.AddCommentRequest.SerializeToString,
                response_deserializer=content__service__pb2.Comment.FromString,
                _registered_method=True)
        self.GetComments = channel.unary_unary(
                '/ContentService/GetComments',
                request_serializer=content__service__pb2.GetCommentsRequest.SerializeToString,
                response_deserializer=content__service__pb2.CommentsList.FromString,
                _registered_method=True)


class ContentServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AddPost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeletePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePost(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetPostById(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetUserPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllPosts(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddComment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetComments(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ContentServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AddPost': grpc.unary_unary_rpc_method_handler(
                    servicer.AddPost,
                    request_deserializer=content__service__pb2.AddPostRequest.FromString,
                    response_serializer=content__service__pb2.Post.SerializeToString,
            ),
            'DeletePost': grpc.unary_unary_rpc_method_handler(
                    servicer.DeletePost,
                    request_deserializer=content__service__pb2.DeletePostRequest.FromString,
                    response_serializer=content__service__pb2.DeletePostResponse.SerializeToString,
            ),
            'UpdatePost': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePost,
                    request_deserializer=content__service__pb2.UpdatePostRequest.FromString,
                    response_serializer=content__service__pb2.Post.SerializeToString,
            ),
            'GetPostById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetPostById,
                    request_deserializer=content__service__pb2.GetPostByIdRequest.FromString,
                    response_serializer=content__service__pb2.Post.SerializeToString,
            ),
            'GetUserPosts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetUserPosts,
                    request_deserializer=content__service__pb2.GetPostsRequest.FromString,
                    response_serializer=content__service__pb2.PostsList.SerializeToString,
            ),
            'GetAllPosts': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllPosts,
                    request_deserializer=content__service__pb2.GetPostsRequest.FromString,
                    response_serializer=content__service__pb2.PostsList.SerializeToString,
            ),
            'AddComment': grpc.unary_unary_rpc_method_handler(
                    servicer.AddComment,
                    request_deserializer=content__service__pb2.AddCommentRequest.FromString,
                    response_serializer=content__service__pb2.Comment.SerializeToString,
            ),
            'GetComments': grpc.unary_unary_rpc_method_handler(
                    servicer.GetComments,
                    request_deserializer=content__service__pb2.GetCommentsRequest.FromString,
                    response_serializer=content__service__pb2.CommentsList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'ContentService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('ContentService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ContentService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AddPost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/AddPost',
            content__service__pb2.AddPostRequest.SerializeToString,
            content__service__pb2.Post.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeletePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/DeletePost',
            content__service__pb2.DeletePostRequest.SerializeToString,
            content__service__pb2.DeletePostResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdatePost(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/UpdatePost',
            content__service__pb2.UpdatePostRequest.SerializeToString,
            content__service__pb2.Post.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetPostById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/GetPostById',
            content__service__pb2.GetPostByIdRequest.SerializeToString,
            content__service__pb2.Post.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetUserPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/GetUserPosts',
            content__service__pb2.GetPostsRequest.SerializeToString,
            content__service__pb2.PostsList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllPosts(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/GetAllPosts',
            content__service__pb2.GetPostsRequest.SerializeToString,
            content__service__pb2.PostsList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AddComment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/AddComment',
            content__service__pb2.AddCommentRequest.SerializeToString,
            content__service__pb2.Comment.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetComments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/ContentService/GetComments',
            content__service__pb2.GetCommentsRequest.SerializeToString,
            content__service__pb2.CommentsList.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
