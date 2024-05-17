from lib.post_repository import PostRepository
from lib.post import Post

"""
When we call PostRepository#all
We get a list of Post objects reflecting the seed data.
"""
def test_get_all_records(db_connection): # See conftest.py to learn what `db_connection` is.
    db_connection.seed("seeds/chitter.sql") # Seed our database with some test data
    repository = PostRepository(db_connection) # Create a new PostRepository

    posts = repository.all() # Get all posts
    # Assert on the results
    assert posts == [
        Post(1, "Hi I'm Alice!", '2024-05-16 15:00:00', 1),
        Post(2, 'Alright, my name is Charlie.', '2024-05-16 15:30:00', 3),
        Post(3, 'Eyo, I am Bob.', '2024-05-16 16:00:00', 2)
    ]

"""
When we call PostRepository#find
We get a single Post object reflecting the seed data.
"""
def test_get_single_post(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = PostRepository(db_connection)

    post = repository.find(3)
    assert post == Post(3, 'Eyo, I am Bob.', '2024-05-16 16:00:00', 2)

"""
When we call PostRepository#create
We get a new post in the database.
"""
def test_create_post(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = PostRepository(db_connection)

    new_post = repository.create(Post(None, "Oh wow I had the first peep on chitter!", '2024-05-16 15:20:00', 1))

    result = repository.all()
    print(result)
    assert result == [
        Post(1, "Hi I'm Alice!", '2024-05-16 15:00:00', 1),
        Post(2, 'Alright, my name is Charlie.', '2024-05-16 15:30:00', 3),
        Post(3, 'Eyo, I am Bob.', '2024-05-16 16:00:00', 2),
        new_post
    ]

"""
When we call PostRepository#delete
We remove a record from the database.
"""
def test_delete_post(db_connection):
    db_connection.seed("seeds/chitter.sql")
    repository = PostRepository(db_connection)
    repository.delete(3)

    result = repository.all()
    assert result == [
        Post(1, "Hi I'm Alice!", '2024-05-16 15:00:00', 1),
        Post(2, 'Alright, my name is Charlie.', '2024-05-16 15:30:00', 3)
    ]
