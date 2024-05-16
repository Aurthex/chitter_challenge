from lib.post import *

def test_create_post_then():
    then = datetime.strptime('2020-05-16 09:05:01', '%Y-%m-%d %H:%M:%S')
    post = Post(0, "test content", then, 1)

    assert post.post_id == 0
    assert post.content == "test content"
    assert post.post_date == then
    assert post.user_id == 1
    assert str(post) == f"Peep({post.post_id}, user {post.author_username}({post.author_name}), peeped {post.content}, on {post.post_date})"

def test_create_post_now():
    now = datetime.now().replace(microsecond=0)
    post = Post(0, "test content", now, 1)

    assert post.post_id == 0
    assert post.content == "test content"
    assert post.post_date == now
    assert post.user_id == 1
    assert str(post) == f"Peep({post.post_id}, user {post.author_username}({post.author_name}), peeped {post.content}, on {post.post_date})"

def test_compare_equal_posts():
    now = datetime.now().replace(microsecond=0)
    post1 = Post(1, "duplicate", now, 2)
    post2 = Post(1, "duplicate", now, 2)

    assert post1 == post2

def test_compare_unequal_posts():
    then = then = datetime.strptime('2020-05-16 09:05:01', '%Y-%m-%d %H:%M:%S')
    now = datetime.now().replace(microsecond=0)

    post1 = Post(2, "could be duplicate?", then, 3)
    post2 = Post(2, "could be duplicate?", now, 3)

    assert post1 != post2