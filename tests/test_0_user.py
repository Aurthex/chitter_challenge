from lib.user import *

def test_make_user():
    user = User(0, "Bob", "bob_test", "bob@bobmail.com", "bobsPass")
    assert user.user_id == 0
    assert user.user_name == "Bob"
    assert user.user_username == "bob_test"
    assert user.email == "bob@bobmail.com"
    assert user.password == "bobsPass"

    assert str(user) == f"User({user.user_id}, {user.user_name}, {user.user_username})"