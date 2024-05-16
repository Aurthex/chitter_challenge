from lib.post import *
from lib.user import *

class PostRepository:

    # We initialise with a database connection
    def __init__(self, connection):
        self._connection = connection

    # Retrieve all posts
    def all(self, get_authors = False):
        if get_authors: return self.all_with_author_info()
        return self.all_without_author_info()
    
    def all_with_author_info(self):
        query = 'SELECT * FROM posts JOIN users ON posts.user_id = users.user_id'
        rows = self._connection.execute(query)
        posts = []
        for row in rows:
            post = Post(row["post_id"], row["content"], row["post_date"], row["user_id"])
            posts.append(post)
        return posts

    def all_without_author_info(self):
        query = 'SELECT * from posts'
        rows = self._connection.execute(query)
        posts = []
        for row in rows:
            post = Post(row["post_id"], row["content"], row["post_date"], row["user_id"])
            posts.append(post)
        return posts

    # Find a single post by their id
    def find(self, post_id):
        rows = self._connection.execute(
            'SELECT * from posts WHERE post_id = %s', [post_id])
        row = rows[0]
        return Post(row["post_id"], row["content"], row["post_date"], row["user_id"])

    # Create a new post
    # Do you want to get its id back? Look into RETURNING id;
    def create(self, post):
        rows = self._connection.execute(
            'INSERT INTO posts (content, post_date, user_id) VALUES (%s, %s, %s) RETURNING post_id', 
            [post.content, post.post_date, post.user_id])
        row = rows[0]
        post.post_id = row['post_id']
        return post

    # Delete an post by their id
    def delete(self, post_id):
        self._connection.execute(
            'DELETE FROM posts WHERE post_id = %s', [post_id])
        return None
