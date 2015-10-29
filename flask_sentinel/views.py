# -*- coding: utf-8 -*-
"""
    flask-sentinel.views
    ~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2015 by Nicola Iarocci.
    :license: BSD, see LICENSE for more details.
"""
import os
from flask import render_template, request, flash

from .core import oauth
from .data import Storage
from .basicauth import requires_basicauth
from .mail import send_email


@oauth.token_handler
def access_token(*args, **kwargs):
    """ This endpoint is for exchanging/refreshing an access token.

    Returns a dictionary or None as the extra credentials for creating the
    token response.

    :param *args: Variable length argument list.
    :param **kwargs: Arbitrary keyword arguments.
    """
    return None


@requires_basicauth
def management():
    """ This endpoint is for vieweing and adding users and clients. """
    error = None
    if request.method == 'POST' and request.form['submit'] == 'Add User':
        email = request.form['email']
        result = Storage.save_user(request.form['username'],
                                   request.form['password'],
                                   email)
        if result['status'] == 'success':
            message = {
                'auto_html': None,
                'auto_text': None,
                'from_email': os.getenv('FROM_EMAIL') or 'from@example.com',
                'from_name': os.getenv('FROM_NAME') or 'Example Name',
                'html': '<p>Example HTML content</p>',
                'subject': 'Your Account is created!',
                'tags': ['user-registration'],
                'to': [{'email': email,
                        'type': 'to'}],
                'track_clicks': True,
                'track_opens': True}
            send_email(message)
        else:
            error = result['message']
    if request.method == 'POST' and request.form['submit'] == 'Add Client':
        Storage.generate_client()
        error = None
    return render_template('management.html', users=Storage.all_users(),
                           clients=Storage.all_clients(), error=error)
