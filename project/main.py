from flask import Blueprint, render_template, url_for, redirect, request,flash
from flask_login import login_required, current_user
from project import db
from project.models import User
from project.forms import UploadAudio
from project.utils import save_audio
from project.audio_reader.Audio_Reader import VideoGenerator

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', "POST"])
@login_required
def profile():
    form = UploadAudio()
    if form.validate_on_submit():
        if form.audiofile.data:
            audio_file = save_audio(form.audiofile.data)
            current_user.audio = audio_file
        db.session.commit()
        return redirect(url_for('main.load'))
    return render_template('profile.html',form=form, name=current_user.name)

@main.route('/load')
@login_required
def load():
    VideoGenerator.covertToVideo('./project/audio_reader/audio/'+current_user.audio)
    return redirect(url_for('main.dashboard'))

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return "Done"

