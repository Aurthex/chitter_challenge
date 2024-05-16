from lib.database_connection import DatabaseConnection
from lib.user import *
import hashlib

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, name, username, email, password):
        # Validation stuff comes before this
        # Hash the password
        binary_password = password.encode("utf-8")
        hashed_password = hashlib.sha256(binary_password).hexdigest()

        # Store the email and hashed password in the database
        rows = self._connection.execute(
            'INSERT INTO users (user_name, user_username, email, password) VALUES (%s, %s, %s, %s) RETURNING user_id',
            [name, username, email, hashed_password])
        row = rows[0]
        return User(row['user_id'], name, username, email, hashed_password)

    def check_password(self, email, password_attempt):
        # Hash the password attempt
        binary_password_attempt = password_attempt.encode("utf-8")
        hashed_password_attempt = hashlib.sha256(binary_password_attempt).hexdigest()

        # Check whether there is a user in the database with the given email
        # and a matching password hash, using a SELECT statement.
        rows = self._connection.execute(
            'SELECT * FROM users WHERE email = %s AND password = %s',
            [email, hashed_password_attempt])

        # If that SELECT finds any rows, the password is correct.
        return len(rows) > 0

    # Retrieve all users
    def all(self):
        rows = self._connection.execute('SELECT * from users')
        users = []
        for row in rows:
            item = User(row["user_id"], row["user_name"], row["user_username"], row["email"], row["password"])
            users.append(item)
        return users

    # Find a single user by their id
    def find(self, user_id):
        rows = self._connection.execute(
            'SELECT * from users WHERE user_id = %s', [user_id])
        row = rows[0]
        return User(row["user_id"], row["user_name"], row["user_username"], row["email"], row["password"])

    # Find a single user by their email
    def find_by_email(self, email):
        rows = self._connection.execute(
            'SELECT * from users WHERE email= %s', [email])
        if len(rows) == 0: return None
        row = rows[0]
        return User(row["user_id"], row["user_name"], row["user_username"], row["email"], row["password"])

    def does_user_email_exist(self, email):
        result = self.find_by_email(email)
        if result == None: return False
        return 

    # Delete an user by their id
    def delete(self, user_id):
        self._connection.execute(
            'DELETE FROM users WHERE user_id = %s', [user_id])
        return None
