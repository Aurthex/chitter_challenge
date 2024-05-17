from datetime import datetime

class Post:
    def __init__(self, post_id, content, post_date, user_id):
        self.post_id = post_id
        self.content = content
        post_date = str(post_date)
        self.post_date = datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S')
        self.user_id = user_id
        self.author_name = user_id
        self.author_username = user_id

    def set_names(self, name, username):
        self.author_name = name
        self.author_username = username

    # This method allows our tests to assert that the objects it expects
    # are the objects we made based on the database records.
    def __eq__(self, other):
        if type(self) != type(other): return False
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print an Artist
    def __repr__(self):
        return f"Peep({self.post_id}, user {self.author_username}({self.author_name}), peeped {self.content}, on {self.post_date})"

    # These next two methods will be used by the controller to check if
    # books are valid and if not show errors to the user.
    def is_valid(self):
        if self.user_id == None or self.user_id == "":
            return False
        if self.content == None or self.content == "":
            return False
        return True

    def generate_errors(self):
        errors = []
        if self.user_id == None or self.user_id == "":
            errors.append("You must be logged in to peep!")
        if self.content == None or self.content == "":
            errors.append("Peeps can't be blank!")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)
        
    def get_tags(self):
        tags = []
        words = self.content.split(' ')
        for word in words:
            if word[0] != '@': continue
            tags.append(word[1:])
        return tags