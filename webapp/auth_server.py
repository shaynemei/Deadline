"""
functions related to user authentication.
"""

from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import flash
from flask import g

from firebase_admin import auth
from functools import wraps

import sys


# middleware to make sure only valid users can perform CRUD
def check_token(view):
    @wraps(view)
    def wrap(*args, **kwargs):
        if not g.user:
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrap


# Sign up a new user
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        error = None
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        elif password != confirm_password:
            error = "Password doesn't match."

        try:
            auth.create_user(
                email=email,
                password=password
            )
        except:
            _, error, _ = sys.exc_info()

        if not error:
            return redirect(url_for("login"))

        # show error message
        flash(error)

    return render_template("signup.html")


# Log in existing user
def login(pb):
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        if not email:
            error = "Email is required"
        elif not password:
            error = "Password is required"
        if not error:
            try:
                session.clear()
                user = pb.auth().sign_in_with_email_and_password(email, password)
                jwt = user['idToken']
                session['api_session_token'] = jwt
                return redirect(url_for('status'))
            except:
                _, error, _ = sys.exc_info()

        flash(error)

    return render_template("login.html")