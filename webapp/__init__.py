from flask import Flask
from flask import render_template
from firebase_admin import auth
from . import db
from . import auth_server


# init the app instance
app = Flask(__name__)

# init connection to Firebase
# pb is used for db operations
# firebase is an admin sdk for validating tokens
firebase, pb = db.init_db()


# a hello page for testing
@app.route('/hello', methods=["GET"])
def hello():
    return "Hello World!"


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


# Test route to check token
@app.route('/api/userinfo', methods=["GET"])
@auth_server.check_token
def userinfo():
    return auth_server.userinfo()


# Api route to sign up a new user
@app.route('/api/signup', methods=["GET", "POST"])
def signup():
    return auth_server.signup()


# Api route to get a new token for a valid user
@app.route('/api/token', methods=["POST"])
def token():
    return auth_server.token(pb)
