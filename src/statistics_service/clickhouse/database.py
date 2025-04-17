from clickhouse_pool import ChPool
from datetime import datetime

class Database:
    def __init__(self, db_params):
        # print(db_params)
        self.pool = ChPool(
            host=db_params["host"],
            port=int(db_params["port"]),
            user=db_params["user"],
            password=db_params["password"],
            database=db_params["database"]
        )
        self._create_tables()
        
    def _create_tables(self):
        """
        Метод для создания таблиц, если они не существуют.
        """
        create_likes_table = """
        CREATE TABLE IF NOT EXISTS Likes (
            userId  UInt32,
            postId  UInt32,
            updatedAt DateTime,
            PRIMARY KEY (userId, postId)
        ) ENGINE = MergeTree()
        ORDER BY (userId, postId);
        """

        create_views_table = """
        CREATE TABLE IF NOT EXISTS Views (
            userId  UInt32,
            postId  UInt32,
            updatedAt DateTime,
            PRIMARY KEY (userId, postId)
        ) ENGINE = MergeTree()
        ORDER BY (userId, postId);
        """

        try:
            with self.pool.get_client() as client:
                client.execute(create_likes_table)
                client.execute(create_views_table)
            # print("DATABASES CREATED")
        except Exception as e:
            raise RuntimeError(f"Ошибка при создании таблиц: {e}")

    def add_like(self, user_id, post_id):
        # print("ДОБАВЛЯЮ ЛАЙК")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_query = """
            INSERT INTO Likes (userId, postId, updatedAt) VALUES
        """
        values_format = f"({user_id}, {post_id}, '{timestamp}')"
        check_query = """
            SELECT count(*) 
            FROM Likes 
            WHERE userId = {user_id}
            AND postId = {post_id}
        """.format(user_id=user_id, post_id=post_id)
        try:
            with self.pool.get_client() as client:
                rows = client.execute(check_query)
                if not rows[0][0]:
                    client.execute(insert_query + values_format)
        except Exception as e:
            # print("ПРОИЗОШЛА ОШИБКА ", e, sep = ' ')
            return None

        like = {
            "user_id": user_id,
            "post_id": post_id,
            "updated_at": timestamp
        }
        return like

    def add_view(self, user_id: int, post_id: int) -> str:
        # print("ДОБАВЛЯЮ ПРОСМОТР")
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert_query = """
            INSERT INTO Views (userId, postId, updatedAt) VALUES
        """
        values_format = f"({user_id}, {post_id}, '{timestamp}')"
        check_query = """
            SELECT count(*) 
            FROM Views 
            WHERE userId = {user_id}
            AND postId = {post_id}
        """.format(user_id=user_id, post_id=post_id)
        try:
            with self.pool.get_client() as client:
                rows = client.execute(check_query)
                if not rows[0][0]:
                    client.execute(insert_query + values_format)
        except Exception as e:
            # print("ПРОИЗОШЛА ОШИБКА ", e, sep = ' ')
            return None

        view = {
            "user_id": user_id,
            "post_id": post_id,
            "updated_at": timestamp
        }
        return view

