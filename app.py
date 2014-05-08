# -*- coding: utf-8 -*-

from urllib import urlencode
import uuid

from flask import (Flask, render_template, request, redirect, url_for, session,
    abort, flash)
from werkzeug.utils import secure_filename

import requests

from config import AGILIQ, SECRET_KEY
from forms import ResumeUploadForm

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

###
# Application Routing
###

@app.route('/')
def home():
    """Render website's home page. """
    return render_template('home.html')


@app.route('/auth/agiliq/', methods=['GET'])
def auth_agiliq():
    """Redirect the user to the OAuth provider (i.e. Agiliq)
    using an URL with a few key OAuth parameters."""
    session['state'] = uuid.uuid1()
    params = urlencode({
        'client_id': AGILIQ['CLIENT_ID'],
        'redirect_uri': AGILIQ['CALLBACK_URL'],
        'state': session['state'],
    })
    auth_url = '%s?%s' % (AGILIQ['AUTHORIZATION_BASE_URL'], params)
    return redirect(auth_url)


@app.route('/logout/', methods=['GET'])
def logout():
    """Logout user from the application."""
    session.clear()
    return redirect(url_for('home'))


@app.route('/callback/agiliq/', methods=['GET'])
def callback_agiliq():
    """Retrieve an access token and save it for subsequent calls."""
    code = request.args.get('code', '')
    state = request.args.get('state', '')

    if not code:
        abort(400)

    try:
        if str(state) != str(session['state']):
            abort(400)
    except KeyError:
        abort(400)

    payload = {
        'client_id': AGILIQ['CLIENT_ID'],
        'client_secret': AGILIQ['CLIENT_SECRET'],
        'code': code,
        'redirect_uri': AGILIQ['CALLBACK_URL'],
    }

    # exchange the provided code for access token
    res = requests.post(AGILIQ['TOKEN_URL'], data=payload)
    data = res.json()
    session['access_token'] = data.get('access_token', '')
    return redirect(url_for('upload_resume'))


@app.route('/upload/', methods=['GET', 'POST'])
def upload_resume():
    """Handles the resume upload functionality."""
    access_token = session.get('access_token', None)

    if not access_token:
        abort(400)

    params = urlencode({
       'access_token': access_token
    })

    upload_url = '%s?%s' % (AGILIQ['UPLOAD_URL'], params)

    form = ResumeUploadForm()

    if form.validate_on_submit():
        payload = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'projects_url': form.projects_url.data,
            'code_url': form.code_url.data,
        }
        resume_data = form.resume.data
        filename = secure_filename(resume_data.filename)
        files = {
            'resume': (filename, resume_data.read(), resume_data.mimetype)
        }
        try:
            res = requests.post(upload_url, files=files, data=payload)
            return redirect(url_for('upload_resume_success'))
        except requests.exceptions.RequestException as e:
            flash('Unable to upload your resume! Try again.')
            return render_template('upload_form.html', form=form)

    return render_template('upload_form.html', form=form)


@app.route('/upload/success/', methods=['GET'])
def upload_resume_success():
    return render_template('upload_success.html')


@app.after_request
def add_header(response):
    """Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes. """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    response.headers['X-Frame-Options'] = 'DENY'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """
    Custom 404 page.
    """
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
