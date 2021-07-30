from classes.RStatus import RStatus
from epsilonModules.ModJob import get_job_applications_by_uid
from epsilonModules.ModTeam import get_user_teams, update_jap_to_rstatus
from epsilonModules.ModUser import *
from classes.Type import Type
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
            if "accept_job" in request.form:
                message = update_jap_to_rstatus(mysql, int(request.form["accept_job"]), RStatus.ACCEPTED)
            elif "decline_job" in request.form:
                message = update_jap_to_rstatus(mysql, int(request.form["decline_job"]), RStatus.DECLINED)
            else:
                data = request.get_json
                if data:
                    name = request.form["name"]
                    description = request.form["description"]
                    contact = request.form["contact"]
                    message = update_user(mysql, uid, name,
                                          description, contact)

        user_details = get_user_by_uid(mysql, uid)
        job_applications = get_job_applications_by_uid(mysql, uid)
        user_type = Type(user_details.type_id).name.replace('_',' ').title()

        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('user_profile.html', user_details=user_details, job_applications=job_applications,
                               message=message, tid=tid, user_type = user_type)
    except ObjectNotExistsError as e:
        return render_template('user_profile.html', user_details=user_details, job_applications=job_applications,
                               message=message, tid=tid, user_type = user_type)
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
