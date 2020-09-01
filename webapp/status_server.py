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

RESOURCES = ['water', 'food', 'metal']

def status():
    try:
        user = auth.verify_id_token(session['api_session_token'])
        g.user = user
    except:
        return redirect(url_for("login"))

    db = webapp.pb.database()

    nickname, group = get_info(user)
    water = get_resource('water')
    food = get_resource('food')
    metal = get_resource('metal')
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
  nickname, group, uid, db = db_setup()

  all_tasks = db.child('users').child(uid).child('tasks').get()

  return json.loads(json.dumps((all_tasks.val())))


def complete_task():
  nickname, group, uid, db = db_setup()

  key = request.form.get("key")
  db.child('users').child(uid).child('tasks').child(key).update({
    'completed': True
  })

  return update_resource(random.randint(0, len(RESOURCES) - 1))


def update_resource(ind, val=10):
  nickname, group, uid, db = db_setup()

  resource = RESOURCES[ind]
  db.child('groups').child(group).child('resources').update({
    resource: get_resource(resource) + 10
  })

  resource_dict = {}
  for resource in RESOURCES:
    resource_dict[resource] = get_resource(resource) 

  return resource_dict


def get_resource(resource):
  nickname, group, uid, db = db_setup()
  return db.child('groups').child(group).child('resources').child(resource).get().val()


def db_setup():
  try:
    user = auth.verify_id_token(session['api_session_token'])
    g.user = user
  except:
    return redirect(url_for("login"))
  
  nickname, group = get_info(user)
  uid = user['user_id']
  db = webapp.pb.database()

  return nickname, group, uid, db