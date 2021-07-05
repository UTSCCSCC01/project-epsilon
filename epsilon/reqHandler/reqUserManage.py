from modules.ModUser import *
from flask import request, render_template, redirect, url_for


def render_user_profile(mysql, uid):
    message = ""
    try:
        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                contact = request.form["contact"]
                message = update_user(mysql, uid, name,
                                      description, contact)
        user_details = get_user_profile(mysql, uid)
        return render_template('userprofile.html', user_details=user_details,
                               message=message)
    except Exception as e:
        return render_template('userprofile.html', message=e)
