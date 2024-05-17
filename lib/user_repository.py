from lib.database_connection import DatabaseConnection
from lib.user import *
import bcrypt
from app import secure_password

class UserRepository:
    def __init__(self, connection):
        self._connection = connection

    def create(self, name, username, email, password):
        # Validation stuff comes before this
        hashed_password = secure_password(password)

        rows = self._connection.execute(
            'INSERT INTO users (user_name, user_username, email, password) VALUES (%s, %s, %s, %s) RETURNING user_id',
            [name, username, email, hashed_password])
        row = rows[0]
        return User(row['user_id'], name, username, email, hashed_password)

    def check_password(self, email, password_attempt):
        # Hash the password attempt
        binary_password_attempt = password_attempt.encode("utf-8")

        # Find password hash for matching email address
        rows = self._connection.execute(
            'SELECT password FROM users WHERE email = %s',
            [email])
        if len(rows) < 1: return False
        hashed_password = (rows[0]['password']).encode('utf-8')
        #hashed_password_attempt = hashlib.sha256(binary_password_attempt).hexdigest()

        return bcrypt.checkpw(binary_password_attempt, hashed_password)

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
        return True
    
    # Find a single user by their email
    def find_by_name(self, name):
        rows = self._connection.execute(
            'SELECT * from users WHERE user_name= %s', [name])
        if len(rows) == 0: return None
        row = rows[0]
        return User(row["user_id"], row["user_name"], row["user_username"], row["email"], row["password"])

    def does_user_name_exist(self, name):
        result = self.find_by_name(name)
        if result is None: return False
        return True

    # Delete an user by their id
    def delete(self, user_id):
        self._connection.execute(
            'DELETE FROM users WHERE user_id = %s', [user_id])
        return None
    
    def secure_password(self, password):

        binary_pass = password.encode('utf-8')

        #   Hashing Password
        hash_password = bcrypt.hashpw(
        password=binary_pass,
        salt = bcrypt.gensalt()
        )

        #bcrypt.checkpw(binary_pass, hash_password)
        return hash_password.decode('utf-8')
    
    def is_valid(self, user):
        is_name_valid = not self.does_user_name_exist(user.user_name)
        is_email_valid = not self.does_user_email_exist(user.email)

        return is_name_valid and is_email_valid
    
    def generate_errors(self, user):
        is_name_valid = not self.does_user_name_exist(user.user_name)
        is_email_valid = not self.does_user_email_exist(user.email)

        errors = []
        if is_name_valid == False:
            errors.append('A user with that name already exists')
        if is_email_valid == False:
            errors.append('A user with that email already exists')
        return errors
    
    def tag_user(self, user_id, post_id):
        self._connection.execute(
            'INSERT INTO posts_users (post_id, user_id) VALUES (%s, %s)',
            [post_id, user_id])
    
    
