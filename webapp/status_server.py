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

import random

import webapp


def status():
    try:
        user = auth.verify_id_token(session['api_session_token'])
        g.user = user
    except:
        return redirect(url_for("login"))

    db = webapp.pb.database()

    nickname, group = get_info(user)
    water = db.child('groups').child(group).child('resources').child('water').get().val()
    food = db.child('groups').child(group).child('resources').child('food').get().val()
    metal = db.child('groups').child(group).child('resources').child('metal').get().val()
    if request.method == "POST":
        # TODO add task to database
        add_task(group, user)
        # return render_template("status.html")
    # else:
        # TODO load user specific data, e.g. tasks, group resources

    return render_template("status.html", nickname=nickname, group=group, water=water, food=food, metal=metal)


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

    key = db.child('users').child(uid).child('tasks').push({
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

  all_tasks = db.child('users').child(uid).child('tasks').get()

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
  db.child('users').child(uid).child('tasks').child(key).update({
    'completed': True
  })

  resource = random.randint(0, 2)
  if resource == 0:
    water = db.child('groups').child(group).child('resources').child('water').get().val()
    db.child('groups').child(group).child('resources').update({
      'water': water + 10
    })
  if resource == 1:
    food = db.child('groups').child(group).child('resources').child('food').get().val()
    db.child('groups').child(group).child('resources').update({
      'food': food + 10
    })
  if resource == 2:
    metal = db.child('groups').child(group).child('resources').child('metal').get().val()
    db.child('groups').child(group).child('resources').update({
      'metal': metal + 10
    })

  # get page to update when this method finishes
  tasks()
  return render_template("status.html")