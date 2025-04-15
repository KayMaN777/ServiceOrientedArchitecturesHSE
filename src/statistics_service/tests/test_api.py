from datetime import datetime
import pytest
import grpc
from unittest.mock import MagicMock

from google.protobuf.timestamp_pb2 import Timestamp
from api.proto.statistics_service_pb2 import (
    ActionRequest,
    ActionResponse
)
from api.proto.statistics_service_pb2_grpc import (
    StatisticsServiceStub,
    add_StatisticsServiceServicer_to_server
)

from concurrent import futures
from api.server import StatisticsService

@pytest.fixture(scope="module")
def mock_db():
    db = MagicMock()
    return db

@pytest.fixture(scope="module")
def grpc_server(mock_db):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_StatisticsServiceServicer_to_server(StatisticsService(mock_db), server)
    port = server.add_insecure_port("[::]:0")
    server.start()
    yield server, port
    server.stop(None)

@pytest.fixture
def grpc_stub(grpc_server):
    _, port = grpc_server
    channel = grpc.insecure_channel(f"localhost:{port}")
    stub = StatisticsServiceStub(channel)
    return stub

@pytest.mark.parametrize(
    "metadata,request_data,expected_code,expected_details",
    [
        # 1) Отсутствуют обязательные поля user_id, post_id в метадате
        ({}, {"user_id": 1, "post_id": 2}, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) Полный набор правильной метадаты -> успешное добавление
        ({"user_id": "1", "post_id": "2"}, {"user_id": 1, "post_id": 2},
         None,  # status code == OK
         None),
        # 3) DB вернул None -> внутренняя ошибка
        ({"user_id": "1", "post_id": "2"}, {"user_id": 1, "post_id": 2}, 
         grpc.StatusCode.INTERNAL,
         "Internal error"),
    ]
)
def test_add_like(grpc_stub, mock_db, metadata, request_data, expected_code, expected_details):
    """
    Проверяем:
      - Валидацию метадаты
      - Успех (OK)
      - Случай внутренних ошибок (None из БД)
    """
    if expected_code is None:
        mock_db.add_like.return_value = {
            "user_id": 1,
            "post_id": 2,
            "updated_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        mock_db.add_like.return_value = None

    grpc_metadata = tuple((k, v) for k, v in metadata.items())

    request = ActionRequest(**{
        "user_id": request_data.get("user_id", 0),
        "post_id": request_data.get("post_id", 0),
    })

    try:
        response = grpc_stub.AddLike(request, metadata=grpc_metadata)
        if expected_code is None:
            assert response.post_id == 2
            assert response.user_id == 1
            assert not response.updated_at.GetCurrentTime() == 0
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получил ошибку: {e.details()}")

@pytest.mark.parametrize(
    "metadata,request_data,expected_code,expected_details",
    [
        # 1) Отсутствуют обязательные поля user_id, post_id в метадате
        ({}, {"user_id": 1, "post_id": 2}, grpc.StatusCode.INVALID_ARGUMENT, "Invalid arguments"),
        # 2) Полный набор правильной метадаты -> успешное добавление
        ({"user_id": "1", "post_id": "2"}, {"user_id": 1, "post_id": 2},
         None,  # status code == OK
         None),
        # 3) DB вернул None -> внутренняя ошибка
        ({"user_id": "1", "post_id": "2"}, {"user_id": 1, "post_id": 2}, 
         grpc.StatusCode.INTERNAL,
         "Internal error"),
    ]
)
def test_add_view(grpc_stub, mock_db, metadata, request_data, expected_code, expected_details):
    """
    Проверяем:
      - Валидацию метадаты
      - Успех (OK)
      - Случай внутренних ошибок (None из БД)
    """
    if expected_code is None:
        mock_db.add_view.return_value = {
            "user_id": 1,
            "post_id": 2,
            "updated_at": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        mock_db.add_view.return_value = None

    grpc_metadata = tuple((k, v) for k, v in metadata.items())

    request = ActionRequest(**{
        "user_id": request_data.get("user_id", 0),
        "post_id": request_data.get("post_id", 0),
    })

    try:
        response = grpc_stub.AddView(request, metadata=grpc_metadata)
        if expected_code is None:
            assert response.post_id == 2
            assert response.user_id == 1
            assert not response.updated_at.GetCurrentTime() == 0
        else:
            pytest.fail(f"Ожидалась ошибка {expected_code}, а метод вернул success.")
    except grpc.RpcError as e:
        if expected_code:
            assert e.code() == expected_code
            assert expected_details in e.details()
        else:
            pytest.fail(f"Ожидался успех, а получил ошибку: {e.details()}")
