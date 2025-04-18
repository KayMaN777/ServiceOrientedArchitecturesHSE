import unittest
from urllib.parse import urlparse
from testcontainers.clickhouse import ClickHouseContainer
from clickhouse_driver import Client
from clickhouse.database import Database


class TestDatabase(unittest.TestCase):
    def setUp(cls) -> None:
        cls.clickhouse = ClickHouseContainer("clickhouse/clickhouse-server:21.8")
        cls.clickhouse.start()

        connection_url = cls.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)

        db_params = {
            "database": parsed_url.path[1:],
            "user": parsed_url.username,
            "password": parsed_url.password,
            "host": parsed_url.hostname,
            "port": str(parsed_url.port)
        }
        cls.db = Database(db_params)

    def tearDown(self):
        self.clickhouse.stop()
    
    def test_tables_are_created(self):
        connection_url = self.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)
        client = Client(
            host=parsed_url.hostname,
            port=str(parsed_url.port),
            user=parsed_url.username,
            password=parsed_url.password,
            database=parsed_url.path[1:]
        )

        likes_exists = client.execute("EXISTS TABLE Likes")
        assert likes_exists[0][0] == 1, "Таблица Likes не создана"

        views_exists = client.execute("EXISTS TABLE Views")
        assert views_exists[0][0] == 1, "Таблица Views не создана"
    
    def test_add_like_inserts_record(self):
        user_id, post_id = 10, 100

        like_data = self.db.add_like(user_id, post_id)
        assert like_data is not None, "Метод add_like вернул None при первом добавлении"

        connection_url = self.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)
        client = Client(
            host=parsed_url.hostname,
            port=str(parsed_url.port),
            user=parsed_url.username,
            password=parsed_url.password,
            database=parsed_url.path[1:]
        )

        rows = client.execute(f"SELECT count(*) FROM Likes WHERE userId={user_id} AND postId={post_id}")
        assert rows[0][0] == 1, "Запись не появилась в таблице Likes после добавления"
    
    def test_add_like_idempotent(self):
        user_id, post_id = 20, 200
        connection_url = self.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)
        client = Client(
            host=parsed_url.hostname,
            port=str(parsed_url.port),
            user=parsed_url.username,
            password=parsed_url.password,
            database=parsed_url.path[1:]
        )

        self.db.add_like(user_id, post_id)
        rows_initial = client.execute(f"SELECT count(*) FROM Likes WHERE userId={user_id} AND postId={post_id}")
        assert rows_initial[0][0] == 1, "Первая запись не была добавлена"

        self.db.add_like(user_id, post_id)
        rows_after_second_call = client.execute(f"SELECT count(*) FROM Likes WHERE userId={user_id} AND postId={post_id}")
        assert rows_after_second_call[0][0] == 1, "Произошло дублирование записи в лайках"

    def test_add_view_inserts_record(self):
        user_id, post_id = 30, 300

        view_data = self.db.add_view(user_id, post_id)
        assert view_data is not None, "Метод add_view вернул None при первом добавлении"

        connection_url = self.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)
        client = Client(
            host=parsed_url.hostname,
            port=str(parsed_url.port),
            user=parsed_url.username,
            password=parsed_url.password,
            database=parsed_url.path[1:]
        )

        rows = client.execute(f"SELECT count(*) FROM Views WHERE userId={user_id} AND postId={post_id}")
        assert rows[0][0] == 1, "Запись не появилась в таблице Views после добавления"

    def test_add_view_idempotent(self):
        user_id, post_id = 40, 400
        connection_url = self.clickhouse.get_connection_url()
        parsed_url = urlparse(connection_url)
        client = Client(
            host=parsed_url.hostname,
            port=str(parsed_url.port),
            user=parsed_url.username,
            password=parsed_url.password,
            database=parsed_url.path[1:]
        )

        self.db.add_view(user_id, post_id)
        rows_initial = client.execute(f"SELECT count(*) FROM Views WHERE userId={user_id} AND postId={post_id}")
        assert rows_initial[0][0] == 1, "Первая запись не была добавлена"

        self.db.add_view(user_id, post_id)
        rows_after_second_call = client.execute(f"SELECT count(*) FROM Views WHERE userId={user_id} AND postId={post_id}")
        assert rows_after_second_call[0][0] == 1, "Произошло дублирование записи в просмотрах"