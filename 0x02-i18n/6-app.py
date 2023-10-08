#!/usr/bin/env python3
"""Localization Module.

This module provides localization support for our web app.

"""

from flask import Flask, request, g
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)

# Configure your Flask app and other settings here...

@babel.localeselector
def get_locale():
    """Determine the user's preferred language."""
    # 1. Locale from URL parameters
    locale = request.args.get('locale')

    # 2. Locale from user settings
    if not locale:
        if hasattr(g, 'user') and g.user:
            locale = g.user.get('locale')

    # 3. Locale from request header
    if not locale:
        locale = request.headers.get('Accept-Language')

    # 4. Default locale
    if not locale:
        locale = app.config['BABEL_DEFAULT_LOCALE']

    return locale

