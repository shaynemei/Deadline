"""
functions related to the user status page
"""

from flask import render_template
from flask import request
from flask import g
from flask import session
from flask import redirect
from flask import url_for

from firebase_admin import auth


def status(pb):
    try:
        user = auth.verify_id_token(session['api_session_token'])
        g.user = user
    except:
        return redirect(url_for("login"))

    if request.method == "POST":
        # TODO add task to database
        return render_template("status.html")
    else:
        # TODO load user specific data, e.g. tasks, group resources
        return render_template("status.html")