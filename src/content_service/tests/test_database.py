import unittest
from urllib.parse import urlparse
from testcontainers.postgres import PostgresContainer
from postgres.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(cls) -> None:
        cls.postgres = PostgresContainer("postgres:13-alpine")
        cls.postgres.start()

        connection_url = cls.postgres.get_connection_url()
        parsed_url = urlparse(connection_url)

        db_params = {
            "database": parsed_url.path[1:],
            "user": parsed_url.username,
            "password": parsed_url.password,
            "host": parsed_url.hostname,
            "port": str(parsed_url.port)
        }

        cls.db = Database(db_params)
        conn = cls.db.connection_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(
            """
            DROP TABLE IF EXISTS Posts;
            CREATE TABLE Posts(
                postId SERIAL PRIMARY KEY,
                userId INTEGER NOT NULL,
                createdAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updatedAt TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                isPrivate BOOLEAN NOT NULL DEFAULT FALSE,
                tags TEXT,
                title TEXT NOT NULL,
                desctiption TEXT,  -- For the INSERT from add_post (typo in original code)
                description TEXT   -- For the SELECT/UPDATE from get_post/update_post
            );
        """,
        )
        conn.commit()
        cursor.close()
        cls.db.connection_pool.putconn(conn)
    
    def tearDown(self):
        self.postgres.stop()
    
    def test_execute_query_success(self):
        status, result = self.db.execute_query("SELECT 1;")
        assert status is True
        assert result == [(1,)]

    def test_execute_query_failure(self):
        status, result = self.db.execute_query("SELECT something_invalid FROM non_existent_table;")
        assert status is False
        assert result is None

    def test_add_post(self):
        new_post = self.db.add_post(user_id=123, title="Test Title", description="Test Description", tags="tag1,tag2", is_private=True)
        assert new_post is not None
        assert new_post["user_id"] == 123
        assert new_post["title"] == "Test Title"
        assert new_post["description"] == "Test Description"
        assert new_post["tags"] == "tag1,tag2"
        assert new_post["is_private"] is True

        new_post_no_tags = self.db.add_post(user_id=456, title="Title No Tags", description="Desc No Tags")
        assert new_post_no_tags is not None
        assert new_post_no_tags["tags"] is None

    def test_get_post_existing(self):
        post = self.db.add_post(user_id=999, title="Get Post Title", description="Get Post Description")
        assert post is not None
        status, rows = self.db.execute_query("""
            SELECT postId FROM Posts WHERE userId=999 ORDER BY postId DESC LIMIT 1
        """)
        assert status is True and rows
        post_id = rows[0][0]

        loaded_post = self.db.get_post(post_id)
        assert loaded_post is not None
        assert loaded_post["post_id"] == post_id
        assert loaded_post["user_id"] == 999
        assert loaded_post["title"] == "Get Post Title"

    def test_get_post_non_existent(self):
        non_existent_id = 999999
        loaded_post = self.db.get_post(non_existent_id)
        assert loaded_post is None

    def test_update_post(self):
        post = self.db.add_post(user_id=1, title="Old Title", description="Old Desc", tags="oldtag", is_private=False)
        assert post is not None
        status, rows = self.db.execute_query("""
            SELECT postId FROM Posts WHERE userId=1 ORDER BY postId DESC LIMIT 1
        """)
        assert status is True and rows
        post_id = rows[0][0]

        updated_data = self.db.update_post(
            post_id=post_id,
            user_id=1,
            title="New Title",
            description="New Description",
            tags="newtag",
            is_private=True
        )
        assert updated_data is not None
        assert updated_data["title"] == "New Title"
        assert updated_data["description"] == "New Description"
        assert updated_data["tags"] == "newtag"
        assert updated_data["is_private"] is True

    def test_delete_post_existing(self):
        post = self.db.add_post(user_id=2, title="Delete Me", description="To be deleted")
        assert post is not None
        status, rows = self.db.execute_query("""
            SELECT postId, userId FROM Posts WHERE userId=2 ORDER BY postId DESC LIMIT 1
        """)
        assert status is True and rows
        post_id = rows[0][0]
        user_id = rows[0][1]

        delete_status = self.db.delete_post(post_id, user_id)
        assert delete_status is True

        post_after_delete = self.db.get_post(post_id)
        assert post_after_delete is None

    def test_delete_post_non_existent(self):
        delete_status = self.db.delete_post(987654, 1)
        assert delete_status is None

    def test_get_user_posts_empty(self):
        posts = self.db.get_user_posts(user_id=1001)
        assert posts == []

    def test_get_users_posts_multiple(self):
        user_id = 300
        self.db.add_post(user_id, "Title1", "Desc1")
        self.db.add_post(user_id, "Title2", "Desc2")
        self.db.add_post(user_id, "Title3", "Desc3")
        posts_all = self.db.get_user_posts(user_id)
        assert len(posts_all) == 3, "Should return exactly 3 inserted posts"

        posts_limited = self.db.get_user_posts(user_id, limit=2, offset=0)
        assert len(posts_limited) == 2

        posts_offset = self.db.get_user_posts(user_id, limit=10, offset=1)
        assert len(posts_offset) == 2

    def test_get_user_posts_zero_limit(self):
        user_id = 400
        self.db.add_post(user_id, "TitleA", "DescA")
        self.db.add_post(user_id, "TitleB", "DescB")
        posts = self.db.get_user_posts(user_id, limit=0)
        assert len(posts) == 0

    def test_get_posts_private_and_public(self):
        self.db.add_post(user_id=10, title="PublicPost", description="Public desc", is_private=False)
        self.db.add_post(user_id=10, title="PrivatePost", description="Private desc", is_private=True)
        self.db.add_post(user_id=20, title="OtherUserPrivate", description="Should not be visible", is_private=True)
        self.db.add_post(user_id=20, title="OtherUserPublic", description="Should be visible", is_private=False)

        posts_for_user10 = self.db.get_posts(user_id=10)
        assert len(posts_for_user10) == 3

        posts_for_user20 = self.db.get_posts(user_id=20)
        assert len(posts_for_user20) == 3

        posts_for_others = self.db.get_posts(user_id=999)
        assert len(posts_for_others) == 2
