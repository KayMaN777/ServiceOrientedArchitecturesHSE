import logging
import psycopg2
from psycopg2 import sql
from psycopg2 import pool
from datetime import datetime

class Database:
    def __init__(self, db_params):
        # print(db_params)
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,             
            maxconn=10,             
            **db_params
        )
        self.logger = logging.getLogger("content_db_wrapper")
        self.logger.info("Initialized connection pool")
    
    def execute_query(self, query:str, params = None) -> tuple[bool, list]:
        self.logger.info("Started query")
        connection = None
        result = None
        status = True
        try:
            connection = self.connection_pool.getconn()
            cursor = connection.cursor()
            cursor.execute(query, params)

            if (query.strip().upper().startswith("SELECT")):
                result = cursor.fetchall()
            else:
                connection.commit()
        except Exception as error:
            self.logger.error(f"Error while query: {error}")
            status = False
        finally:
            if connection:
                cursor.close()
                self.connection_pool.putconn(connection)
        self.logger.info("Ended query")
        return status, result
    
    def add_post(self, user_id, title, description, tags=None, is_private=False):
        timestamp = datetime.utcnow()
        query = """
            INSERT INTO Posts (userId, createdAt, updatedAt, title, description, tags, isPrivate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (user_id, timestamp, timestamp, title, description, tags, is_private,)
        status, _ = self.execute_query(query, params)
        if not status:
            return None
        response = {
            "user_id": user_id,
            "title": title,
            "created_at": timestamp,
            "updated_at": timestamp,
            "description": description,
            "tags": tags,
            "is_private": is_private
        }
        return response
    
    def delete_post(self, post_id, user_id):
        check_query = """
            SELECT 1
            FROM Posts
            WHERE postId = %s AND userId = %s
        """
        status, result = self.execute_query(check_query, (post_id, user_id))
        if not status or not result:
            return None
        
        query = """
            DELETE FROM Posts
            WHERE postId = %s AND userId = %s
        """
        params = (post_id, user_id,)
        status, _ = self.execute_query(query, params)
        if not status:
            return None
        return status

    def update_post(self, post_id, user_id, title = None, description = None, is_private = None, tags = None):
        check_query = """
            SELECT 1
            FROM Posts
            WHERE postId = %s AND userId = %s
        """
        status, result = self.execute_query(check_query, (post_id, user_id))
        if not status or not result:
            return None
        
        columns_to_update = []
        params = []
        response = {}
        timestamp = datetime.utcnow()
        if title is not None:
            columns_to_update.append("title = %s")
            params.append(title)
            response["title"] = title

        if description is not None:
            columns_to_update.append("description = %s")
            params.append(description)
            response["description"] = description

        if is_private is not None:
            columns_to_update.append("isPrivate = %s")
            params.append(is_private)
            response["is_private"] = is_private

        if tags is not None:
            columns_to_update.append("tags = %s")
            params.append(tags)
            response["tags"] = tags
        
        columns_to_update.append("updatedAt = %s")
        response["updated_at"] = timestamp
        params.append(timestamp)
        params.append(post_id)
        params.append(user_id)
        query = """
            Update Posts
            SET {0}
            WHERE postId = %s AND userId = %s
        """.format(", ".join(columns_to_update))
        status, _ = self.execute_query(query, params)
        
        if not status:
            return None
        
        return response

    def get_post(self, post_id):
        query = """
            SELECT postId, userId, createdAt, updatedAt, isPrivate, tags, title, description
            FROM Posts
            WHERE postId = %s
        """
        params = (post_id,)
        status, responce = self.execute_query(query, params)
        if not status or not responce:
            return None
        post = {
            "post_id": responce[0][0],
            "user_id": responce[0][1],
            "created_at": responce[0][2],
            "updated_at": responce[0][3],
            "is_private": responce[0][4],
            "tags": responce[0][5],
            "title": responce[0][6],
            "description": responce[0][7]
        }
        return post

    def get_user_posts(self, user_id, limit=100, offset=0):
        query = """
            SELECT postId, userId, createdAt, updatedAt, isPrivate, tags, title, description
            FROM Posts
            WHERE userId = %s
            ORDER BY createdAt DESC
            LIMIT %s OFFSET %s
        """
        params = (user_id, limit, offset,)
        status, response = self.execute_query(query, params)
        if not status:
            return None
        posts = []
        for post in response:
            post_info = {
                "post_id": post[0],
                "user_id": post[1],
                "created_at": post[2],
                "updated_at": post[3],
                "is_private": post[4],
                "tags": post[5],
                "title": post[6],
                "description": post[7]
            }
            posts.append(post_info)
        return posts

    def get_posts(self, user_id, limit=100, offset=0):
        query = """
            SELECT postId, userId, createdAt, updatedAt, isPrivate, tags, title, description
            FROM Posts
            WHERE (isPrivate = FALSE OR userId = %s)
            ORDER BY createdAt DESC
            LIMIT %s OFFSET %s
        """
        params = (user_id, limit, offset,)
        status, response = self.execute_query(query, params)
        if not status:
            return None
        posts = []
        for post in response:
            post_info = {
                "post_id": post[0],
                "user_id": post[1],
                "created_at": post[2],
                "updated_at": post[3],
                "is_private": post[4],
                "tags": post[5],
                "title": post[6],
                "description": post[7]
            }
            posts.append(post_info)
        return posts

    def add_comment(self, user_id, post_id, description):
        timestamp = datetime.utcnow()
        query = """
            INSERT INTO Comments (userId, postId, createdAt, updatedAt, description, tags)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (user_id, post_id, timestamp, timestamp, description,)
        status, _ = self.execute_query(query, params)
        if not status:
            return None
        response = {
            "user_id": user_id,
            "post_id": post_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "description": description,
        }
        return response
    
    def get_comments(self, user_id, limit=100, offset=0):
        query = """
            SELECT postId, userId, createdAt, updatedAt, description
            FROM Comments
            WHERE (postId = %s)
            ORDER BY createdAt DESC
            LIMIT %s OFFSET %s
        """
        params = (user_id, limit, offset,)
        status, response = self.execute_query(query, params)
        if not status:
            return None
        comments = []
        for comment in response:
            comment_info = {
                "post_id": comment[0],
                "user_id": comment[1],
                "created_at": comment[2],
                "updated_at": comment[3],
                "description": comment[4]
            }
            comments.append(comment_info)
        return comments