"""Very simple Flask app that allows setting and retrieving boolean values."""

# pip install -U flask flask-cors

import os
from os import path

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

TOGGLES_DIR = path.join(path.dirname(path.realpath(__file__)), r'toggles')

with open(path.join(path.dirname(path.realpath(__file__)), r'PASSKEY'), 'r', -1, 'utf-8') as f:
    PASSKEY = f.readlines()[0].strip()

@app.get('/toggle/get/<toggle>')
def get_toggle(toggle):
    """Get the value of a toggle (if the passkey matches the PASSKEY env var)."""
    toggle_path = path.join(TOGGLES_DIR, toggle)
    if path.exists(toggle_path):
        return 'true'
    else:
        return 'false'

@app.get('/toggle/set/<toggle>/<value>/<passkey>')
def set_toggle(toggle, value, passkey):
    """Set the value of a toggle (if the passkey matches the PASSKEY env var)."""
    if passkey != PASSKEY:
        raise PermissionError("Invalid passkey")

    toggle_path = path.join(TOGGLES_DIR, toggle)

    if not path.exists(TOGGLES_DIR):
        os.makedirs(TOGGLES_DIR)

    if value == 'true':
        with open(toggle_path, 'w') as _:  #pylint: disable=W1514
            pass
        return 'true'
    elif value == 'false':
        if path.exists(toggle_path):
            os.remove(toggle_path)
        return 'false'

if __name__ == '__main__':
    app.run()
