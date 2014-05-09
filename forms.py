from flask_wtf import Form
from wtforms import validators, TextField
from flask_wtf.file import FileField, FileAllowed, FileRequired

from config import ALLOWED_EXTENSIONS


class ResumeUploadForm(Form):
    first_name = TextField('First Name', [
            validators.required(),
            validators.Length(min=3, max=25)
        ])
    last_name = TextField('Last Name', [
            validators.required(),
            validators.Length(min=3, max=25)
        ])
    projects_url = TextField('Project Url', [
            validators.required(),
            validators.URL(),
        ])
    code_url = TextField('Code Url', [
            validators.required(),
            validators.URL(),
        ])
    resume = FileField('Resume', validators=[
        FileRequired(),
        FileAllowed(ALLOWED_EXTENSIONS, 'File type not allowed!')
    ])
