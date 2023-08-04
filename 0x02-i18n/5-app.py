#!/usr/bin/env python3
"""User login system mock."""

from flask import Flask, render_template, g, request
from typing import Dict, Optional

app = Flask(__name__)

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


@app.route('/', strict_slashes=False)
def index() -> str:
    """Render the index template."""
    return render_template('5-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

