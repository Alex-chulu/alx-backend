#!/usr/bin/env python3
"""User login system mock."""

from flask import Flask, render_template, g, request
from flask_babel import Babel, _
from typing import Dict, Optional
import pytz

app = Flask(__name__)
babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id: int) -> Optional[Dict[str, str]]:
    """Get user dictionary by ID."""
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """Execute before all other functions."""
    user_id = int(request.args.get("login_as", 0))
    g.user = get_user(user_id)


@babel.localeselector
def get_locale() -> str:
    """Get the locale for translations."""
    # Check locale from URL parameters
    locale = request.args.get("locale")
    if locale and locale in babel.list_translations():
        return locale

    # Check locale from user settings
    if g.user and g.user.get("locale") in babel.list_translations():
        return g.user.get("locale")

    # Check locale from request header
    return request.accept_languages.best_match(babel.list_translations())


@babel.timezoneselector
def get_timezone() -> str:
    """Get the time zone for formatting dates and times."""
    # Check timezone from URL parameters
    timezone = request.args.get("timezone")
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Check timezone from user settings
    if g.user and g.user.get("timezone"):
        try:
            pytz.timezone(g.user.get("timezone"))
            return g.user.get("timezone")
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    # Default to UTC
    return "UTC"


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render the index template."""
    return render_template('7-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

