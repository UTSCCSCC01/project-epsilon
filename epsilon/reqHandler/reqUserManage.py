from epsilonModules.ModTeam import get_user_teams
from epsilonModules.ModUser import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user


def render_user_profile(mysql: MySQL):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :return template for user profile page.
    """
    uid = current_user.uid
    message = ""
    try:
        tid = -1
        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                contact = request.form["contact"]
                message = update_user(mysql, uid, name,
                                      description, contact)
        user_details = get_user_profile(mysql, uid)
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('user_profile.html', user_details=user_details,
                               message=message, tid= tid)
    except ObjectNotExistsError as e:
        return render_template('user_profile.html', user_details=user_details,
                               message=message, tid= tid)
    except Exception as e:
        return render_template('user_profile.html', message=e)

def load_User_O(mysql: MySQL, uid: int):
    """
    Returns a user object to be verified by the session
    :param mysql: mysql db.
    :param uid: uid of user
    :return user object.
    """
    user = get_user_by_uid(mysql, uid)
    return user
