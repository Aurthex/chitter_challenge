import re

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
        if type(self) != type(other): return False
        return self.__dict__ == other.__dict__

    # This method makes it look nicer when we print a User
    def __repr__(self):
        return f"User({self.user_id}, {self.user_name}, {self.user_username})"
    
    def is_valid(self):
        isNameValid = bool(re.match('[a-zA-Z\s]+$', self.user_name))
        isUserNameValid = self.user_username.isalnum()
        isPasswordValid = self.validate_password()

        return isNameValid and isUserNameValid and isPasswordValid

    def generate_errors(self):
        isNameValid = bool(re.match('[a-zA-Z\s]+$', self.user_name))
        isUserNameValid = self.user_username.isalnum()
        isPasswordValid = self.validate_password()

        errors = []
        if isNameValid == False:
            errors.append("Name must contain only letters and spaces")
        if isUserNameValid == False:
            errors.append("Usernames can contains only letters and numbers")
        if isPasswordValid == False:
            errors.append("Passwords must be at least 8 characters long and contains both letters and numbers")
        return errors

    def validate_password(self):
        pw = self.password
        if len(pw) < 8: return False
        if pw.isalpha() or pw.isnumeric(): return False
        return True