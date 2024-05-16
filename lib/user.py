class User:
    def __init__(self, id, name, username, email, password):
        self.user_id = id
        self.user_name = name
        self.user_username = username
        self.email = email
        self.password = password

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print a User
    def __repr__(self):
        return f"User({self.user_id}, {self.user_name}, {self.user_username})"