from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField

class UploadAudio(FlaskForm):
    audiofile = FileField('Upload Audio', validators=[FileAllowed(['mp3'])])
    submit = SubmitField('Upload')