from flask import Flask, render_template
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def get_locale():
    # Implement logic to determine the user's preferred language
    # For simplicity, we'll use 'en' (English) as the default language
    return 'en'

@app.route('/')
def home():
    current_time = get_current_time()  # Implement this function to get the current time
    return render_template('home.html', current_time=current_time)

if __name__ == '__main__':
    app.run()

