# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: content_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'content_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63ontent_service.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"\xce\x01\n\x04Post\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12.\n\ncreated_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12.\n\nupdated_at\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x12\n\nis_private\x18\x05 \x01(\x08\x12\x0c\n\x04tags\x18\x06 \x03(\t\x12\r\n\x05title\x18\x07 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x08 \x01(\t\"g\n\x0e\x41\x64\x64PostRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0c\n\x04tags\x18\x04 \x03(\t\x12\x12\n\nis_private\x18\x05 \x01(\x08\"$\n\x11\x44\x65letePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\"%\n\x12\x44\x65letePostResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"j\n\x11UpdatePostRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\x12\r\n\x05title\x18\x02 \x01(\t\x12\x13\n\x0b\x64\x65scription\x18\x03 \x01(\t\x12\x0c\n\x04tags\x18\x04 \x03(\t\x12\x12\n\nis_private\x18\x05 \x01(\x08\"%\n\x12GetPostByIdRequest\x12\x0f\n\x07post_id\x18\x01 \x01(\x05\"A\n\x0fGetPostsRequest\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\r\n\x05limit\x18\x02 \x01(\x05\x12\x0e\n\x06offset\x18\x03 \x01(\x05\"!\n\tPostsList\x12\x14\n\x05posts\x18\x01 \x03(\x0b\x32\x05.Post2\x99\x02\n\x0e\x43ontentService\x12!\n\x07\x41\x64\x64Post\x12\x0f.AddPostRequest\x1a\x05.Post\x12\x35\n\nDeletePost\x12\x12.DeletePostRequest\x1a\x13.DeletePostResponse\x12\'\n\nUpdatePost\x12\x12.UpdatePostRequest\x1a\x05.Post\x12)\n\x0bGetPostById\x12\x13.GetPostByIdRequest\x1a\x05.Post\x12,\n\x0cGetUserPosts\x12\x10.GetPostsRequest\x1a\n.PostsList\x12+\n\x0bGetAllPosts\x12\x10.GetPostsRequest\x1a\n.PostsListb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'content_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_POST']._serialized_start=59
  _globals['_POST']._serialized_end=265
  _globals['_ADDPOSTREQUEST']._serialized_start=267
  _globals['_ADDPOSTREQUEST']._serialized_end=370
  _globals['_DELETEPOSTREQUEST']._serialized_start=372
  _globals['_DELETEPOSTREQUEST']._serialized_end=408
  _globals['_DELETEPOSTRESPONSE']._serialized_start=410
  _globals['_DELETEPOSTRESPONSE']._serialized_end=447
  _globals['_UPDATEPOSTREQUEST']._serialized_start=449
  _globals['_UPDATEPOSTREQUEST']._serialized_end=555
  _globals['_GETPOSTBYIDREQUEST']._serialized_start=557
  _globals['_GETPOSTBYIDREQUEST']._serialized_end=594
  _globals['_GETPOSTSREQUEST']._serialized_start=596
  _globals['_GETPOSTSREQUEST']._serialized_end=661
  _globals['_POSTSLIST']._serialized_start=663
  _globals['_POSTSLIST']._serialized_end=696
  _globals['_CONTENTSERVICE']._serialized_start=699
  _globals['_CONTENTSERVICE']._serialized_end=980
# @@protoc_insertion_point(module_scope)
