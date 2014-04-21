# -*- coding: utf-8 -*-

from urllib import urlencode
import uuid

from flask import (Flask, render_template, request, redirect, url_for, session,
    abort, flash)
from flask.json import jsonify

import requests

from config import AGILIQ, allowed_file, SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

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
        abort(401)

    try:
        if str(state) != str(session['state']):
            abort(401)
    except KeyError:
        abort(401)

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
    access_token = session.get('access_token', '')

    if not access_token:
        abort(401)

    params = urlencode({
       'access_token': access_token
    })

    # for testing only
    AGILIQ['UPLOAD_URL'] = 'http://httpbin.org/post'

    upload_url = '%s?%s' % (AGILIQ['UPLOAD_URL'], params)

    if request.method == 'POST':
        payload = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'projects_url': request.form['projects_url'],
            'code_url': request.form['code_url'],
        }

        uploaded_file = request.files['resume']
        if uploaded_file and allowed_file(uploaded_file.filename):
            files = {
                'resume': (uploaded_file.filename, uploaded_file.stream,
                    uploaded_file.mimetype)
            }
            res = requests.post(upload_url, files=files, data=payload)
            return render_template('upload_success.html')

        flash('Application submission failed! Try again.')
        return render_template('upload_form.html')

    return render_template('upload_form.html')


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
