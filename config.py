from os import environ

AGILIQ = {
    'CLIENT_ID': environ.get('AGILIQ_CLIENT_ID'),
    'CLIENT_SECRET': environ.get('AGILIQ_CLIENT_SECRET'),
    'AUTHORIZATION_BASE_URL': 'http://join.agiliq.com/oauth/authorize/',
    'TOKEN_URL': 'http://join.agiliq.com/oauth/access_token/',
    'CALLBACK_URL': 'http://join-agiliq.herokuapp.com/callback/agiliq/',
    'UPLOAD_URL': 'http://join.agiliq.com/api/resume/upload/',
}

SECRET_KEY = environ.get('SECRET_KEY')

ALLOWED_EXTENSIONS = ['txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc',
    'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp',
    'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml', 'pdf', 'md', 'rst']
