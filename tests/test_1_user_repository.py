from lib.user_repository import UserRepository
from lib.user import User

"""
When we call UserRepository#all
We get a list of User objects reflecting the seed data.
"""
def test_get_all_records(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/chitter.sql") # Seed our database with some test data
    repository = UserRepository(db_connection) # Create a new UserRepository

    users = repository.all() # Get all users
    # Assert on the results
    assert users == [
        User(1, "Alice", "alice010", "alice@alicemail.com", "p455w0rd"),
        User(2, "Bob", "bob_test", "bob@bobmail.com", "bobsPass"),
        User(3, "Charlie", "cha-cha-slide", "charlie@cmail.com", "123456")
    ]

"""
When we call UserRepository#find
We get a single User object reflecting the seed data.
"""
def test_get_single_user(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = UserRepository(db_connection)

    user = repository.find(3)
    assert user == User(3, "Charlie", "cha-cha-slide", "charlie@cmail.com", "123456")

"""
When we call UserRepository#create
We get a new user in the database.
"""
def test_create_user(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = UserRepository(db_connection)

    new_user = repository.create("Daniel", "D_town", "DanDaDanDan@dmail.com", "D")
    result = repository.all()
    print(result)
    expected = [
        User(1, "Alice", "alice010", "alice@alicemail.com", "p455w0rd"),
        User(2, "Bob", "bob_test", "bob@bobmail.com", "bobsPass"),
        User(3, "Charlie", "cha-cha-slide", "charlie@cmail.com", "123456"),
        new_user
    ]
    for i in range (len(result)):
        assert result[i] == expected[i]

"""
When we call UserRepository#delete
We remove a record from the database.
"""
def test_delete_user(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = UserRepository(db_connection)
    repository.delete(3)

    result = repository.all()
    assert result == [
        User(1, "Alice", "alice010", "alice@alicemail.com", "p455w0rd"),
        User(2, "Bob", "bob_test", "bob@bobmail.com", "bobsPass")
    ]
