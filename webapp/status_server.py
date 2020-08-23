"""
functions related to the user status page
"""

from flask import render_template
from flask import request
from flask import g
from flask import session
from flask import redirect
from flask import url_for
import time
import json

from firebase_admin import auth

import webapp


def status():
    try:
        user = auth.verify_id_token(session['api_session_token'])
        g.user = user
    except:
        return redirect(url_for("login"))

    nickname, group = get_info(user)
    if request.method == "POST":
        # TODO add task to database
        add_task(group, user)
        # return render_template("status.html")
    # else:
        # TODO load user specific data, e.g. tasks, group resources

    return render_template("status.html", nickname=nickname, group=group)


def get_info(user):
  db = webapp.pb.database()
  uid = user['user_id']

  nickname = db.child('users').child(uid).child('nickname').get().val()
  group = db.child('users').child(uid).child('group').get().val()

  return nickname, group


def add_task(group, user):
  if request.method == "POST":
    db = webapp.pb.database()

    content = request.form.get('task')
    uid = user['user_id']

    key = db.child('groups').child(group).child(uid).child('tasks').push({
      'content': content,
      'timestamp': time.time(),
      'completed': False
    })

def tasks():
  try:
      user = auth.verify_id_token(session['api_session_token'])
      g.user = user
  except:
      return redirect(url_for("login"))

  nickname, group = get_info(user)
  uid = user['user_id']
  db = webapp.pb.database()

  all_tasks = db.child('groups').child(group).child(uid).child('tasks').get()
  print(all_tasks.val())

  return json.loads(json.dumps((all_tasks.val())))


def complete_task():
  try:
    user = auth.verify_id_token(session['api_session_token'])
    g.user = user
  except:
    return redirect(url_for("login"))
  
  nickname, group = get_info(user)
  uid = user['user_id']
  db = webapp.pb.database()

  key = request.form.get("key")
  print(request.form['key'])
  db.child('groups').child(group).child(uid).child('tasks').child(key).update({
    'completed': True
  })
  task = db.child('groups').child(group).child(uid).child('tasks').child(key).get()
  print(task.val())
  tasks()
  return render_template("status.html")