from epsilonModules.ModUser import *
from flask import request, render_template, redirect, url_for


def render_user_profile(mysql: MySQL, uid: int):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :param uid: uid of user
    :return template for user profile page.
    """
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
        return render_template('user_profile.html', user_details=user_details,
                               message=message)
    except Exception as e:
        return render_template('user_profile.html', message=e)
