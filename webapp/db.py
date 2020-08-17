import json
import firebase_admin
import pyrebase


# Connect to firebase
def init_db():
    cred = firebase_admin.credentials.Certificate('firebaseAdminConfig.json')
    firebase = firebase_admin.initialize_app(cred)
    pb = pyrebase.initialize_app(json.load(open('firebaseConfig.json')))
    return firebase, pb
