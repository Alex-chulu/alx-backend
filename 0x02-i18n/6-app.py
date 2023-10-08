#!/usr/bin/env python3

from flask import request
from typing import Optional
from flask_babel import _
import babel
import pytz
from werkzeug.exceptions import NotFound

@babel.localeselector
def get_locale() -> Optional[str]:
    """Determine the user's preferred locale.
    
    The function prioritizes locale selection in the following order:
    1. Locale from URL parameters.
    2. Locale from user settings.
    3. Locale from the request header (Accept-Language).
    4. Default locale.
    
    Returns:
        str: The selected locale or None if none of the above conditions are met.
    """
    # Check if the locale is provided in URL parameters
    locale = request.args.get('locale')
    if locale and locale in supported_locales:
        return locale

    # Check if the locale is set in user settings (implement this function)
    user_locale = get_user_locale()
    if user_locale and user_locale in supported_locales:
        return user_locale

    # Check the request header for the Accept-Language header
    header_locale = request.accept_languages.best_match(supported_locales)
    if header_locale and header_locale in supported_locales:
        return header_locale

    # Default to the app's default locale
    return app.config['BABEL_DEFAULT_LOCALE']

def get_user_locale() -> Optional[str]:
    """Get the user's preferred locale from user settings.

    Returns:
        str: The user's preferred locale or None if not set.
    """
    # Implement logic to fetch the user's locale from user settings
    # Example: user_locale = current_user.preferred_locale
    # Modify this part based on your application's user model and settings
    user_locale = None  # Replace with actual user locale retrieval logic
    return user_locale

# List of supported locales in your application
supported_locales = ['en', 'fr']

# Initialize Flask app, Babel extension, and configure Babel
app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'

