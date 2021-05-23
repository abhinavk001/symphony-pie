import os
from os import environ
import secrets
from flask import current_app
import pyrebase


def save_audio(form_audio):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_audio.filename)
    audio_fn = random_hex+f_ext
    audio_path = os.path.join(current_app.root_path, 'audio_reader/audio', audio_fn)
    form_audio.save(audio_path)
    return f_name, audio_fn

firebaseConfig = {
        
    }

""" def storage():
    firebase = pyrebase.initialize_app(firebaseConfig)
    fstore = firebase.storage()
    return fstore """

def get_from_firebase(filename):
    firebase = pyrebase.initialize_app(firebaseConfig)
    fstore = firebase.storage()
    url = fstore.child('videos/'+filename).get_url(None)
    return url

def store_to_firebase(filename):
    firebase = pyrebase.initialize_app(firebaseConfig)
    fstore = firebase.storage()
    fstore.child("videos/" + filename).put(filename)
