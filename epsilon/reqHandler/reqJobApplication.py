from epsilonModules.ModJobApplication import get_applicant_profile
from flask_mysqldb import MySQL
from epsilonModules.ModTeam import get_user_teams
from epsilonModules.ModUser import *
from flask import app, request, render_template, redirect, url_for
from flask_login import current_user

def render_applicant_profile(mysql: MySQL, jap_id: int):
    """
    Handler for applicant profile.
    :param mysql: mysql db.
    :param jap_id: the jap_id of the application.
    :return template for applicant profile page.
    """
    message = ""
    try:
        tid = -1
        applicant = get_applicant_profile(mysql, jap_id)
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('applicant_profile.html', applicant=applicant,
                               message=message, tid= tid)
    except Exception as e:
        return render_template('applicant_profile.html', message=e, tid= tid)
