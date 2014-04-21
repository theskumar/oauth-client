import os

AGILIQ = {
    'CLIENT_ID': os.environ['AGILIQ_CLIENT_ID'],
    'CLIENT_SECRET': os.environ['AGILIQ_CLIENT_SECRET'],
    'AUTHORIZATION_BASE_URL': 'http://join.agiliq.com/oauth/authorize/',
    'TOKEN_URL': 'http://join.agiliq.com/oauth/access_token/',
    'CALLBACK_URL': 'http://join-agiliq.herokuapp.com/callback/agiliq/',
    'UPLOAD_URL': 'http://join.agiliq.com/api/resume/upload/',
}

SECRET = os.environ['SECRET']

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx', 'md'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
