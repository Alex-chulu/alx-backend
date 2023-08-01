#!/usr/bin/env python3
"""Basic Flask app with a single route and an index.html template"""

from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index() -> str:
    """Render the index.html template."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run()

