import os
from flask import Flask, request, render_template, redirect, session
from lib.database_connection import *
from lib.user_repository import *
from lib.post_repository import *
import bcrypt

# Create a new Flask app
app = Flask(__name__)


@app.route('/signup')
def sign_up():
    if session['user_id'] != None:
        return redirect('/')
    return render_template('signup.html')
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
        return render_template('signup.html', name = user_name, username = user_username, errors=user.generate_errors()), 400

    # Check for database validity and if not valid, show the form again with errors
    if not repository.is_valid(user):
        return render_template('signup.html', name = user_name, username = user_username, errors=repository.generate_errors(user)), 400

    # Save the user to the database
    user = repository.create(user_name, user_username, email, password)

    # Redirect to the user to login
    return redirect(f"/login")

# This route simply returns the login page
@app.route('/login')
def login():
    return render_template('login.html')

# This route receives login information (email and password) as POST parameters,
# checks whether the credentials are valid, and if so finds the user in the database
# using the email. If all goes well, it stores the user's ID in the session
# and shows a success page.
@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    if repository.check_password(email, password):
        user = repository.find_by_email(email)
        # Set the user ID in session
        session['user_id'] = user.user_id
        session['user_name'] = user.user_name
        return redirect('/')

    else:
        return render_template('login.html', errors='Incorrect Email or Password')

    
@app.route('/logout')
def logout():
    session['user_id'] = None
    session['user_name'] = None
    return redirect('/')


# This route is an example of a "authenticated-only" route. It can be accessed 
# only if a user is signed-in (if we have user information in session).
@app.route('/account_page')
def account_page():
    if 'user_id' not in session:
        # No user id in the session so the user is not logged in.
        return redirect('/login')
    else:
        # The user is logged in, display their account page.
        return render_template('account.html')
    
@app.route('/')
def feed():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    posts = repository.all(True)
    if 'user_id' not in session:
        session['user_id'] = None
    if 'user_name' not in session:
        session['user_name'] = None
    return render_template('posts.html', posts=posts, user=session['user_name'])
    
@app.route('/', methods=['POST'])
def feed_post():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    posts = repository.all(True)

    # Get the fields from the request form
    content = request.form['content']
    user_id = session['user_id']
    published = datetime.now().replace(microsecond=0)

    # Create a post object
    post = Post(None, content, published, user_id)

    if content == None or content == "":
        return render_template('posts.html', user=session['user_name'], posts=posts, content = content, errors="Content cannot be empty"), 400

    if user_id == None:
        return render_template('posts.html', user=session['user_name'], posts=posts, content = content, errors="You must be signed in to post!"), 400

    # Save the user to the database
    repository.create(post)

    # Get tags
    tags= post.get_tags()

    repository = UserRepository(connection)
    tagged_users = []
    for tag in tags:
        user = repository.find_by_name(tag)
        if user != None: repository.tag_user(user.user_id, post.post_id)
    
    # Redirect to the user to login
    return redirect(f"/")

@app.route('/notifications')
def notifications():
    connection = get_flask_database_connection(app)
    repository = PostRepository(connection)
    if 'user_id' not in session:
        return redirect(f"/")
    if 'user_name' not in session:
        return redirect(f"/")
    new_posts = repository.all_unseen_tagged_with_author_info(session['user_id'])
    all_posts = repository.all_tagged_with_author_info(session['user_id'])
    return render_template('notifications.html', new_posts=new_posts, all_posts =all_posts, user=session['user_name'])
    

# Hash the password
def secure_password(password):
        binary_pass = password.encode('utf-8')
        hash_password = bcrypt.hashpw(binary_pass, bcrypt.gensalt())
        return hash_password.decode('utf-8')
        

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))