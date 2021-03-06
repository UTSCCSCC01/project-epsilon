import os
from epsilonModules.ModPic import get_pic
from epsilonModules.ModJobApplication import get_applicant_profile
from flask_mysqldb import MySQL
from epsilonModules.ModTeam import get_user_teams
from epsilonModules.ModUser import *
from flask import app, request, render_template, redirect, url_for
from epsilonModules.ModJob import apply_to_job, check_existence_of_application
from flask_login import current_user
import traceback


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
            pfp = get_pic(mysql, applicant.uid)
            if pfp:
                if os.path.exists("./static/pfp.png"):
                    os.remove("./static/pfp.png")
                with open('./static/pfp.png', 'wb') as wf:
                    wf.write(pfp)
        return render_template('applicant_profile.html', applicant=applicant,
                               message=message, tid=tid, pic=pfp)
    except Exception as e:
        return render_template('applicant_profile.html', message=e, tid=tid)


def render_job_application(mysql: MySQL, jid: int):
    """
    Handler for page where user applies to a specific job.
    This handler assumes current user is eligible to apply for a job.
    :param: mysql: mysql db
    :return: template
    """
    try:
        if request.method == "POST":
            skills = request.form["skills"]
            message = apply_to_job(mysql=mysql, jid=jid, uid=current_user.uid,
                                   skills=skills)
            return render_template("job_application.html", message=message)
        else:
            return render_template("job_application.html")

    except Exception as e:
        traceback.print_exc()
        return render_template("job_application.html", error=e)
