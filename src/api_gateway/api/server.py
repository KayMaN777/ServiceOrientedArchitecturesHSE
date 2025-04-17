
import json
from flask import Flask, request, Response, jsonify
import requests
import os
import grpc
import api.proto.content_service_pb2_grpc as content_service_pb2_grpc
import api.proto.content_service_pb2 as content_service_pb2
from http import HTTPStatus
from google.protobuf import json_format

class ApiGatewayServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.user_service_address = f"http://{os.getenv('USER_API_HOST')}:{os.getenv('USER_API_PORT')}"
        grpc_host = os.getenv('CONTENT_API_HOST')
        grpc_port = os.getenv('CONTENT_API_PORT')
        channel = grpc.insecure_channel(f'{grpc_host}:{grpc_port}')
        self.content_stub = content_service_pb2_grpc.ContentServiceStub(channel)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/register', methods=['POST'])
        def register():
            url = f'{self.user_service_address}/register'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
    
        @self.app.route('/login', methods=['POST'])
        def login():
            url = f'{self.user_service_address}/login'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))

        @self.app.route('/update', methods=['PUT'])
        def update():
            url = f'{self.user_service_address}/update'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
        
        @self.app.route('/profile', methods=['GET'])
        def get_profile():
            url = f'{self.user_service_address}/profile'
            response = requests.request(
                method=request.method,
                url=url,
                headers={key: value for key, value in request.headers if key != 'Host'},
                json=request.get_json(silent=True),
                params=request.args
            )
                
            return Response(response.content, status=response.status_code, headers=dict(response.headers))
        
        @self.app.route('/post', methods=['GET', 'POST', 'PUT', 'DELETE'])
        def handle_content_request():
            profile_responce = get_profile()
            if profile_responce.status_code != HTTPStatus.OK:
                return profile_responce

            match request.method:
                case 'GET':
                    req_data = request.get_json(silent=True) or {}
                    if "postId" not in req_data:
                        return jsonify({
                            "error": "Bad request",
                            "message": "Missing field: postId"
                        }), HTTPStatus.BAD_REQUEST
                    metadata = [("post_id", 'True')]
                    get_post_req = content_service_pb2.GetPostByIdRequest(
                        post_id=req_data['postId']
                    )
                    try:
                        response = self.content_stub.GetPostById(get_post_req, metadata=metadata)
                        resp_json = {
                            "postId":response.post_id,
                            "userId":response.user_id,
                            "createdAt":json_format.MessageToJson(response.created_at),
                            "updatedAt":json_format.MessageToJson(response.updated_at),
                            "isPrivate":response.is_private,
                            "tags":list(response.tags),
                            "title":response.title,
                            "description":response.description
                        }
                        resp_json = json.dumps(resp_json, ensure_ascii=False)
                        Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                    except grpc.RpcError as e:
                        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                            return jsonify({
                                "error": "Invalid arguments",
                                "message":""
                            }), HTTPStatus.BAD_REQUEST
                        else:
                            return jsonify({
                                "error":"Internal error",
                                "message":""
                            }), HTTPStatus.INTERNAL_SERVER_ERROR
                case 'POST':
                    req_data = request.get_json(silent=True) or {}
                    required_fields = ['userId', 'title', 'description']
                    missing_fields = [field for field in required_fields if field not in req_data]
                    if missing_fields:
                        return jsonify({
                            "error": "Bad Request",
                            "message": f"Missing fields: {', '.join(missing_fields)}"
                        }), HTTPStatus.BAD_REQUEST
                    metadata = [('user_id', 'True'), ('title', 'True'), ('description', 'True')]
                    if 'tags' in req_data:
                        metadata.append(('tags', 'True'))
                    if 'isPrivate' in req_data:
                        metadata.append(('is_private', 'True'))
                    add_post_req = content_service_pb2.AddPostRequest(
                        user_id=req_data.get("userId", 0),
                        title=req_data.get("title", ""),
                        description=req_data.get("description", ""),
                        tags=req_data.get("tags", []),
                        is_private=req_data.get("isPrivate", False)
                    )
                    try:
                        response = self.content_stub.AddPost(add_post_req, metadata=metadata)
                        resp_json = {
                            "userId":response.user_id,
                            "createdAt":json_format.MessageToJson(response.created_at),
                            "updatedAt":json_format.MessageToJson(response.updated_at),
                            "isPrivate":response.is_private,
                            "tags":list(response.tags),
                            "title":response.title,
                            "description":response.description
                        }
                        resp_json = json.dumps(resp_json, ensure_ascii=False)
                        return Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                    except grpc.RpcError as e:
                        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                            return jsonify({
                                "error": "Invalid arguments",
                                "message":""
                            }), HTTPStatus.BAD_REQUEST
                        else:
                            return jsonify({
                                "error":"Internal error",
                                "message":""
                            }), HTTPStatus.INTERNAL_SERVER_ERROR
                case 'PUT':
                    req_data = request.get_json(silent=True) or {}
                    required_fields = ['postId', 'userId']
                    missing_fields = [field for field in required_fields if field not in req_data]
                    if missing_fields:
                        return jsonify({
                            "error": "Bad Request",
                            "message": f"Missing fields: {', '.join(missing_fields)}"
                        }), HTTPStatus.BAD_REQUEST
                    metadata = [('post_id', 'True'), ('user_id', 'True')]
                    for field in ['title', 'description', 'tags']:
                        if field in req_data:
                            metadata.append((field, 'True'))
                    if 'isPrivate' in req_data:
                        metadata.append(('is_private', 'True'))
            
                    update_post_req = content_service_pb2.UpdatePostRequest(
                        post_id=req_data.get("postId", 0),
                        title=req_data.get("title", ""),
                        description=req_data.get("description", ""),
                        tags=req_data.get("tags", []),
                        is_private=req_data.get("isPrivate", False)
                    )

                    try:
                        response = self.content_stub.UpdatePost(update_post_req, metadata=metadata)
                        resp_json = {
                            "postId":req_data.get("postId", 0),
                            "userId":req_data.get("userId", 0),
                            "updatedAt":json_format.MessageToJson(response.updated_at),
                        }
                        if 'title' in req_data:
                            resp_json['title'] = response.title
                        if 'description' in req_data:
                            resp_json['description'] = response.description
                        if 'tags' in req_data:
                            resp_json['tags'] = list(response.tags)
                        if 'isPrivate' in req_data:
                            resp_json['isPrivate'] = response.is_private

                        resp_json = json.dumps(resp_json, ensure_ascii=False)
                        return Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                    except grpc.RpcError as e:
                        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                            return jsonify({
                                "error": "Invalid arguments",
                                "message":""
                            }), HTTPStatus.BAD_REQUEST
                        else:
                            return jsonify({
                                "error":"Internal error",
                                "message":""
                            }), HTTPStatus.INTERNAL_SERVER_ERROR
                case 'DELETE':
                    req_data = request.get_json(silent=True) or {}
                    if "postId" not in req_data:
                        return jsonify({
                            "error": "Bad request",
                            "message": "Missing field: postId"
                        }), HTTPStatus.BAD_REQUEST
                    metadata = [("post_id", 'True')]
                    delete_post_req = content_service_pb2.DeletePostRequest(
                        post_id=req_data["postId"]
                    )
                    try:
                        response = self.content_stub.DeletePost(delete_post_req, metadata=metadata)
                        resp_json = {
                            "success":response.success
                        }    
                        resp_json = json.dumps(resp_json, ensure_ascii=False)
                        return Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                    except grpc.RpcError as e:
                        if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                            return jsonify({
                                "error": "Invalid arguments",
                                "message":""
                            }), HTTPStatus.BAD_REQUEST
                        else:
                            return jsonify({
                                "error":"Internal error",
                                "message":""
                            }), HTTPStatus.INTERNAL_SERVER_ERROR
                case _:
                    return jsonify({
                        "error": "Bad request",
                        "message": ""
                    }), HTTPStatus.BAD_REQUEST
        
        @self.app.route('/posts/user', methods=['GET'])
        def get_user_posts():
            profile_responce = get_profile()
            if profile_responce.status_code != HTTPStatus.OK:
                return profile_responce

            if request.method == 'GET':
                req_data = request.get_json(silent=True) or {}
                required_fields = ['userId', 'limit', 'offset']
                missing_fields = [field for field in required_fields if field not in req_data]
                if missing_fields:
                    return jsonify({
                        "error": "Bad Request",
                        "message": f"Missing fields: {', '.join(missing_fields)}"
                    }), HTTPStatus.BAD_REQUEST
                metadata = [('user_id', 'True'), ('limit', 'True'), ('offset', 'True')]
                get_posts_req = content_service_pb2.GetPostsRequest(
                    user_id=req_data['userId'],
                    limit=req_data['limit'],
                    offset=req_data['offset']
                )
                try:
                    response = self.content_stub.GetUserPosts(get_posts_req, metadata=metadata)
                    posts_list = []
                    for post in response.posts:
                        posts_list.append({
                            "post_id": post.post_id,
                            "user_id": post.user_id,
                            "created_at": json_format.MessageToJson(post.created_at),
                            "updated_at": json_format.MessageToJson(post.updated_at),
                            "is_private": post.is_private,
                            "tags": list(post.tags),
                            "title": post.title,
                            "description": post.description
                        })
                    resp_json = {"posts": posts_list}
                    resp_json = json.dumps(resp_json, ensure_ascii=False)
                    return Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                except grpc.RpcError as e:
                    if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                        return jsonify({
                            "error": "Invalid arguments",
                            "message":""
                        }), HTTPStatus.BAD_REQUEST
                    else:
                        return jsonify({
                            "error":"Internal error",
                            "message":""
                        }), HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                return jsonify({
                        "error": "Bad request",
                        "message": ""
                    }), HTTPStatus.BAD_REQUEST
    
        @self.app.route('/posts/all', methods=['GET'])
        def get_all_posts():
            profile_responce = get_profile()
            if profile_responce.status_code != HTTPStatus.OK:
                return profile_responce

            if request.method == 'GET':
                req_data = request.get_json(silent=True) or {}
                required_fields = ['userId', 'limit', 'offset']
                missing_fields = [field for field in required_fields if field not in req_data]
                if missing_fields:
                    return jsonify({
                        "error": "Bad Request",
                        "message": f"Missing fields: {', '.join(missing_fields)}"
                    }), HTTPStatus.BAD_REQUEST
                metadata = [('user_id', 'True'), ('limit', 'True'), ('offset', 'True')]
                get_posts_req = content_service_pb2.GetPostsRequest(
                    user_id=req_data['userId'],
                    limit=req_data['limit'],
                    offset=req_data['offset']
                )
                try:
                    response = self.content_stub.GetAllPosts(get_posts_req, metadata=metadata)
                    posts_list = []
                    for post in response.posts:
                        posts_list.append({
                            "post_id": post.post_id,
                            "user_id": post.user_id,
                            "created_at": json_format.MessageToJson(post.created_at),
                            "updated_at": json_format.MessageToJson(post.updated_at),
                            "is_private": post.is_private,
                            "tags": list(post.tags),
                            "title": post.title,
                            "description": post.description
                        })
                    resp_json = {"posts": posts_list}
                    resp_json = json.dumps(resp_json, ensure_ascii=False)
                    return Response(resp_json, status=HTTPStatus.OK, content_type='application/json; charset=utf-8')
                except grpc.RpcError as e:
                    if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                        return jsonify({
                            "error": "Invalid arguments",
                            "message":""
                        }), HTTPStatus.BAD_REQUEST
                    else:
                        return jsonify({
                            "error":"Internal error",
                            "message":""
                        }), HTTPStatus.INTERNAL_SERVER_ERROR
            else:
                return jsonify({
                        "error": "Bad request",
                        "message": ""
                    }), HTTPStatus.BAD_REQUEST

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

