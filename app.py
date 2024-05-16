import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import *
from lib.user_repository import *
from lib.post_repository import *

# Create a new Flask app
app = Flask(__name__)

# Creates a new user
@app.route('/signup', methods=['POST'])
def create_user():
    # Set up the database connection and repository
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    # Get the fields from the request form
    user_name= request.form['name']
    user_username= request.form['username']
    email = request.form['email']
    password = request.form['password']

    # Create a user object
    user = User(None, user_name, user_username, email, password)

    # Check for internal validity and if not valid, show the form again with errors
    if not user.is_valid():
        return render_template('signup.html', user=user, errors=user.generate_errors()), 400

    # Check for database validity and if not valid, show the form again with errors
    if not repository.is_valid(user):
        return render_template('signup.html', user=user, errors=repository.generate_errors(user)), 400

    # Save the user to the database
    user = repository.create(user)

    # Redirect to the user to login
    return redirect(f"/login")