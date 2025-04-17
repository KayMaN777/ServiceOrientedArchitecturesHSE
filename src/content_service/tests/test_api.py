from datetime import datetime
import pytest
import grpc
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp

from api.proto.content_service_pb2 import (
    Post,
    DeletePostResponse,
    PostsList,
    GetPostByIdRequest,
    GetPostsRequest,
    AddPostRequest,
    DeletePostRequest,
    UpdatePostRequest
)
from api.proto.content_service_pb2_grpc import (
    ContentServiceStub,
    add_ContentServiceServicer_to_server
)

from concurrent import futures
from api.server import ContentService

@pytest.fixture(scope="module")
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture(scope="module")
def grpc_server(mock_db):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_ContentServiceServicer_to_server(ContentService(mock_db), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    yield server, port
    server.stop(None)

@pytest.fixture
def grpc_stub(grpc_server):
    _, port = grpc_server
    channel = grpc.insecure_channel(f"localhost:{port}")
    stub = ContentServiceStub(channel)
    return stub

@pytest.mark.parametrize(
    "metadata,request_data,expected_code,expected_details",
    [
        # 1) Отсутствуют обязательные поля user_id, title, description в метадате
        ({}, {"user_id": 1, "title": "Title", "description": "Desc"}, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) Полный набор правильной метадаты -> успешное добавление
        ({"user_id": "1", "title": "SomeTitle", "description": "SomeDesc", "tags": "true"}, 
         {"user_id": 1, "title": "SomeTitle", "description": "SomeDesc", "tags": ["tag1", "tag2"], "is_private": False},
         None,  # status code == OK
         None),
        # 3) DB вернул None -> внутренняя ошибка
        ({"user_id": "1", "title": "SomeTitle", "description": "SomeDesc"}, 
         {"user_id": 1, "title": "SomeTitle", "description": "SomeDesc"}, 
         grpc.StatusCode.INTERNAL,
         "Internal error"),
    ]
)
def test_add_post(grpc_stub, mock_db, metadata, request_data, expected_code, expected_details):
    """
    Проверяем:
      - Валидацию метадаты
      - Успех (OK)
      - Случай внутренних ошибок (None из БД)
    """
    if expected_code is None:
        mock_db.add_post.return_value = {
            "post_id": 10,
            "user_id": request_data["user_id"],
            "title": request_data["title"],
            "description": request_data["description"],
            "tags": request_data.get("tags", []),
            "is_private": request_data.get("is_private", False),
            "created_at": datetime.utcnow()
        }
    else:
        mock_db.add_post.return_value = None

    grpc_metadata = tuple((k, v) for k, v in metadata.items())

    request = AddPostRequest(**{
        "user_id": request_data.get("user_id", 0),
        "title": request_data.get("title", ""),
        "description": request_data.get("description", ""),
        "tags": request_data.get("tags", []),
        "is_private": request_data.get("is_private", False),
    })

    try:
        response = grpc_stub.AddPost(request, metadata=grpc_metadata)
        if expected_code is None:
            assert response.post_id == 10
            assert response.title == request_data["title"]
            assert response.description == request_data["description"]
            assert not response.created_at.GetCurrentTime() == 0
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получил ошибку: {e.details()}")

@pytest.mark.parametrize(
    "metadata,post_id,db_return,expected_code,expected_details",
    [
        # 1) Нет post_id в метадате
        ({}, 100, True, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) post_id < 0
        ({"post_id": "1"}, -10, True, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 3) DB вернул None -> INTERNAL
        ({"post_id": "1"}, 1, None, grpc.StatusCode.INTERNAL, "Internal error"),
        # 4) Успешное удаление
        ({"post_id": "1"}, 1, True, None, None),
    ]
)
def test_delete_post(grpc_stub, mock_db, metadata, post_id, db_return, expected_code, expected_details):
    mock_db.delete_post.return_value = db_return

    grpc_metadata = tuple((k, v) for k, v in metadata.items())
    request = DeletePostRequest(post_id=post_id)

    try:
        response = grpc_stub.DeletePost(request, metadata=grpc_metadata)
        if expected_code is None:
            # Успех
            assert response.success == True
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получили ошибку: {e.details()}")

@pytest.mark.parametrize(
    "metadata,post_id,request_data,db_return,expected_code,expected_details",
    [
        # 1) Нет post_id
        ({}, 100, {}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) post_id < 0
        ({"post_id": "100"}, -1, {}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 3) DB вернул None -> INTERNAL 
        ({"post_id": "100", "title": "upd"}, 100, {"title": "upd"}, None, grpc.StatusCode.INTERNAL, "Internal error"),
        # 4) Успешное обновление
        ({"post_id": "100", "title": "newTitle", "description": "desc"}, 100, 
         {"title": "newTitle", "description": "desc"}, 
         {
             "post_id": 100,
             "title": "newTitle",
             "description": "desc",
             "is_private": False,
             "tags": [],
             "updated_at": datetime.utcnow()
         },
         None, None),
    ]
)
def test_update_post(grpc_stub, mock_db, metadata, post_id, request_data, db_return, expected_code, expected_details):
    mock_db.update_post.return_value = db_return

    grpc_metadata = tuple((k, v) for k, v in metadata.items())

    request = UpdatePostRequest(
        post_id=post_id,
        title=request_data.get("title", ""),
        description=request_data.get("description", ""),
        tags=request_data.get("tags", []),
        is_private=request_data.get("is_private", False)
    )

    try:
        response = grpc_stub.UpdatePost(request, metadata=grpc_metadata)
        if expected_code is None:
            assert response.post_id == post_id
            assert response.title == request_data["title"]
            assert response.description == request_data["description"]
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получили ошибку: {e.details()}")

@pytest.mark.parametrize(
    "metadata,post_id,db_return,expected_code,expected_details",
    [
        # 1) Нет post_id
        ({}, 10, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) post_id < 0
        ({"post_id": "10"}, -2, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 3) DB = None -> INTERNAL
        ({"post_id": "10"}, 10, None, grpc.StatusCode.INTERNAL, "Internal error"),
        # 4) Успешное возвращение
        ({"post_id": "10"}, 10,
         {
             "post_id": 10,
             "user_id": 1,
             "title": "SomeTitle",
             "description": "SomeDescription",
             "tags": ["abc"],
             "is_private": False
         },
         None, None),
    ]
)
def test_get_post_by_id(grpc_stub, mock_db, metadata, post_id, db_return, expected_code, expected_details):
    mock_db.get_post.return_value = db_return

    grpc_metadata = tuple((k, v) for k, v in metadata.items())
    request = GetPostByIdRequest(post_id=post_id)

    try:
        response = grpc_stub.GetPostById(request, metadata=grpc_metadata)
        if expected_code is None:
            assert response.post_id == db_return["post_id"]
            assert response.title == db_return["title"]
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получили ошибку: {e.details()}")

@pytest.mark.parametrize(
    "metadata,request_data,db_return,expected_code,expected_details",
    [
        # 1) Нет user_id
        ({}, {"user_id": 1, "limit": 10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) user_id < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": -1, "limit": 10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 3) limit < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": -10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 4) offset < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": 10, "offset": -1}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
    ]
)
def test_get_user_posts_invalid_args(grpc_stub, mock_db, metadata, request_data, db_return, expected_code, expected_details):
    mock_db.get_user_posts.return_value = db_return
    grpc_metadata = tuple((k,v) for k,v in metadata.items())

    request = GetPostsRequest(
        user_id=request_data["user_id"],
        limit=request_data["limit"],
        offset=request_data["offset"],
    )

    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetUserPosts(request, metadata=grpc_metadata)
    e = exc_info.value
    assert e.code() == expected_code
    assert expected_details in e.details()


@pytest.mark.parametrize(
    "metadata,request_data,db_return",
    [
        # Успешный вариант
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": 10, "offset": 0}, []),
        # DB вернула None
    ]
)
def test_get_user_posts_success_or_internal(grpc_stub, mock_db, metadata, request_data, db_return):
    # Два сценария: DB = список постов (OK) / DB = None (INTERNAL)
    grpc_metadata = tuple((k,v) for k,v in metadata.items())

    mock_db.get_user_posts.return_value = db_return

    request = GetPostsRequest(
        user_id=request_data["user_id"],
        limit=request_data["limit"],
        offset=request_data["offset"],
    )

    if db_return is None:
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.GetUserPosts(request, metadata=grpc_metadata)
        e = exc_info.value
        assert e.code() == grpc.StatusCode.INTERNAL
        assert "Internal error" in e.details()
    else:
        response = grpc_stub.GetUserPosts(request, metadata=grpc_metadata)
        assert isinstance(response, PostsList)
        assert len(response.posts) == len(db_return)

@pytest.mark.parametrize(
    "metadata,request_data,db_return,expected_code,expected_details",
    [
       # 1) Нет user_id
        ({}, {"user_id": 1, "limit": 10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) user_id < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": -1, "limit": 10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 3) limit < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": -10, "offset": 0}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 4) offset < 0
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": 10, "offset": -1}, None, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
    ]
)
def test_get_all_posts_invalid_args(grpc_stub, mock_db, metadata, request_data, db_return, expected_code, expected_details):
    mock_db.get_posts.return_value = db_return
    grpc_metadata = tuple((k,v) for k,v in metadata.items())

    request = GetPostsRequest(
        user_id=request_data["user_id"],
        limit=request_data["limit"],
        offset=request_data["offset"],
    )

    with pytest.raises(grpc.RpcError) as exc_info:
        grpc_stub.GetAllPosts(request, metadata=grpc_metadata)
    e = exc_info.value
    assert e.code() == expected_code
    assert expected_details in e.details()


@pytest.mark.parametrize(
    "metadata,request_data,db_return",
    [
        # Успешный вариант
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": 10, "offset": 0}, []),
        # DB вернула None
        ({"user_id": "1", "limit": "10", "offset": "0"}, {"user_id": 1, "limit": 10, "offset": 0}, None),
    ]
)
def test_get_all_posts_success_or_internal(grpc_stub, mock_db, metadata, request_data, db_return):
    grpc_metadata = tuple((k,v) for k,v in metadata.items())

    mock_db.get_posts.return_value = db_return

    request = GetPostsRequest(
        user_id=request_data["user_id"],
        limit=request_data["limit"],
        offset=request_data["offset"],
    )

    if db_return is None:
        # Ожидаем INTERNAL
        with pytest.raises(grpc.RpcError) as exc_info:
            grpc_stub.GetAllPosts(request, metadata=grpc_metadata)
        e = exc_info.value
        assert e.code() == grpc.StatusCode.INTERNAL
        assert "Internal error" in e.details()
    else:
        # Ожидаем успех
        response = grpc_stub.GetAllPosts(request, metadata=grpc_metadata)
        assert isinstance(response, PostsList)
        assert len(response.posts) == len(db_return)