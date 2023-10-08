#!/usr/bin/env python3
"""A Flask app with internationalization support and user preferences.

This Flask app demonstrates internationalization support and allows users to
set their preferred locale for the web page. It also maintains user-specific
timezones and other user-related information.

Features:
- Localization support with Flask-Babel.
- User preferences for locale and timezone.
- Secure secret key for session management.

Usage:
1. Start the app by running this script.
2. Access the home page at http://localhost:5000/.
3. Set your preferred locale by appending '?locale=en' or '?locale=fr' to the URL.
4. Select a user by appending '?login_as=<user_id>' to the URL.

Make sure to install the required Flask and Flask-Babel libraries.

Attributes:
    app (Flask): The Flask application.
    babel (Babel): The Babel extension for localization.

"""

from flask_babel import Babel
from typing import Union, Dict
from flask import Flask, render_template, request, g

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change to your secret key
babel = Babel(app)

# Define user data with locale and timezone preferences
users = {
    1: {"name": "Alice", "locale": "en", "timezone": "US/Eastern"},
    2: {"name": "Bob", "locale": "fr", "timezone": "Europe/Paris"},
    3: {"name": "Charlie", "locale": "es", "timezone": "Europe/Madrid"},
    4: {"name": "David", "locale": None, "timezone": "UTC"},
}

def get_user() -> Union[Dict, None]:
    """Retrieves a user based on a user id.

    Args:
        None

    Returns:
        Union[Dict, None]: A dictionary containing user data or None if not found.

    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None

@app.before_request
def before_request() -> None:
    """Performs routines before each request's resolution.

    Args:
        None

    Returns:
        None

    """
    user = get_user()
    g.user = user

@babel.localeselector
def get_locale() -> str:
    """Retrieves the locale for a web page.

    The locale is determined based on URL parameters, user settings, request header,
    or falls back to the default locale.

    Args:
        None

    Returns:
        str: The selected locale.

    """
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])

@app.route('/')
def get_index() -> str:
    """The home/index page.

    Args:
        None

    Returns:
        str: The HTML content of the home page.

    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

