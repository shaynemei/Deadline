from flask import Flask
from flask import render_template
from flask import request
from firebase_admin import auth
from . import db
from functools import wraps


# init the app instance
app = Flask(__name__)

# init connection to Firebase
# pb is used for db operations
# firebase is an admin sdk for validating tokens
firebase, pb = db.init_db()


# middleware to make sure only valid users can perform CRUD
def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'}, 400
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            request.user = user
        except:
            return {'message':'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap


# a hello page for testing
@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/')
def index():
    return render_template('index.html')


# Test route to check token
@app.route('/api/userinfo')
@check_token
def userinfo():
    return {'data': "TEST USER DATA"}, 200


# Api route to sign up a new user
@app.route('/api/signup')
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        return {'message': 'Error missing email or password'}, 400
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return {'message': f'Successfully created user {user.uid}'}, 200
    except Exception as e:
        return {'message': e}, 400


# Api route to get a new token for a valid user
@app.route('/api/token')
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except Exception as e:
        return {'message': e}, 400
