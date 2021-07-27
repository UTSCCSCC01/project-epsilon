from epsilonModules.ModCompany import *
from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template, redirect, url_for
from flask_login import current_user


def render_company_profile(mysql: MySQL, name:str=""):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :param tid: tid of company
    :return template for company profile page.
    """
    message = ""
    try:
        user_team = [0, 0, 0]
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            user_team = [user_teams[0].tid,
                         user_teams[0].uid,
                         user_teams[0].rid]

        if name == "":
            tid = user_team[0]
        else:
            company_details = get_company_profile_by_name(mysql, name)
            tid = company_details[0]

        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                message = update_company(mysql, tid, name,
                                         description)
        company_details = get_company_profile(mysql, tid)
        return render_template('company_profile.html', company_details=company_details,
                               message=message, user_team=user_team, tid=tid)
    except Exception as e:
        return render_template('company_profile.html', message=e)
