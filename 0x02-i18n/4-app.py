#!/usr/bin/env python3
"""Flask app with Babel configuration, language selection, and translations"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext

app = Flask(__name__)
babel = Babel(app)

class Config:
    """Config class to set available languages and Babel settings"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)

@babel.localeselector
def get_locale():
    """Determine the best match with the supported languages or use the forced locale"""
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def index():
    """Render the index.html template with translated messages."""
    return render_template('3-index.html',
                           home_title=gettext("Welcome to Holberton"),
                           home_header=gettext("Hello world!"))

if __name__ == '__main__':
    app.run()

