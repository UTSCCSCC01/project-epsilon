from flask_login import logout_user
from flask import redirect, url_for

def render_logout():
    logout_user()
    return redirect(url_for('hello'))