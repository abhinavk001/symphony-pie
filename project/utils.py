import os
from os import environ
import secrets
from flask import current_app
import pyrebase


def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex+f_ext
    audio_path = os.path.join(current_app.root_path, 'audio_reader/audio', audio_fn)
    form_audio.save(audio_path)
    return audio_fn

""" firebaseConfig = {
    'apiKey': environ.get('apiKey'),
  'authDomain': environ.get('authDomain'),
  'projectId': "symphony-pie",
  'storageBucket': environ.get('storageBucket'),
  'messagingSenderId': environ.get('messagingSenderId'),
  'appId': environ.get('appId'),
  'measurementId': environ.get('measurementId')
    }

def storage():
    firebase = pyrebase.initialize_app(firebaseConfig)
    fstore = firebase.storage()
    return fstore

def save_to_firebase(filename):
    firebase = pyrebase.initialize_app(firebaseConfig)
    fstore = firebase.storage()
    url = fstore.child('images/'+current_user).get_url(None)
    return url """
