"""
Initialise flask instance and define routes.
"""

from flask import Flask
from flask import render_template
from flask import session
from flask import redirect
from flask import url_for

from . import db
from . import auth_server
from . import status_server

import secrets


# init the app instance
app = Flask(__name__)

# set random secret key
secret = secrets.token_urlsafe(32)
app.secret_key = secret

# init connection to Firebase
# pb is used for db operations
# firebase is an admin sdk for validating tokens
firebase, pb = db.init_db()


# Root page
@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"])
def signup():
    return auth_server.signup()


@app.route('/login', methods=["GET", "POST"])
def login():
    return auth_server.login(pb)


@app.route('/logout', methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))


@auth_server.check_token
@app.route('/status', methods=["GET", "POST"])
def status():
    return status_server.status()


@app.route('/tasks', methods=["GET", "POST"])
def tasks():
    return status_server.tasks()
