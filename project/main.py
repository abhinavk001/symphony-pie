import os
from flask import Blueprint, render_template, url_for, redirect, request,flash
from flask_login import login_required, current_user
from project import db
from project.models import User, Video
from project.forms import UploadAudio
from project.utils import save_audio, store_to_firebase, get_from_firebase
from project.audio_reader.Audio_Reader import VideoGenerator

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET', "POST"])
@login_required
def upload():
    form = UploadAudio()
    if form.validate_on_submit():
        if form.audiofile.data:
            org_name, audio_file = save_audio(form.audiofile.data)
            filename,_=os.path.splitext(audio_file)
            file = Video(filename=filename+'.mp4', audio_name=org_name, author=current_user)
            db.session.add(file)
            db.session.commit()
            current_user.audio = audio_file
        db.session.commit()
        return redirect(url_for('main.load'))
    return render_template('profile.html',form=form, name=current_user.name)

@main.route('/load')
@login_required
def load():
    vid_file_name = VideoGenerator.covertToVideo('./project/audio_reader/audio/'+current_user.audio, current_user.audio)
    store_to_firebase(vid_file_name)
    os.remove(vid_file_name)
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    videos = Video.query.filter_by(author=user)
    return render_template('dashboard.html', videos=videos, user=user, get_from_firebase=get_from_firebase)



