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

import webapp


def status():
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
        nickname, group = get_info(user)

        return render_template("status.html", nickname=nickname, group=group)


def get_info(user):
  db = webapp.pb.database()
  uid = user['user_id']

  nickname = db.child('users').child(uid).child('nickname').get().val()
  group = db.child('users').child(uid).child('group').get().val()

  return nickname, group