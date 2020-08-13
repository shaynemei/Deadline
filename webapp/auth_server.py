from flask import render_template
from flask import request
from firebase_admin import auth
from functools import wraps


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
            return {'message': 'Invalid token provided.'}, 400
        return f(*args, **kwargs)
    return wrap


# Test route to check token
def userinfo():
    return {'data': "TEST USER DATA"}, 200


# Api route to sign up a new user
def signup():
    if request.method == "POST":
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
    else:
        # TODO: signup page not created
        # renders index page for now
        return render_template("index.html")


def token(pb):
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = pb.auth().sign_in_with_email_and_password(email, password)
        jwt = user['idToken']
        return {'token': jwt}, 200
    except Exception as e:
        return {'message': e}, 400