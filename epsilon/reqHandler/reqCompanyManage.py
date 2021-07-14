from epsilonModules.ModCompany import *
from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template, redirect, url_for
from flask_login import current_user


def render_company_profile(mysql: MySQL):
    """
    Handler for company profile.
    :param mysql: mysql db.
    :param tid: tid of company
    :return template for company profile page.
    """
    message = ""
    try:
        teams = get_user_teams(mysql, current_user.uid)
        company_details = get_company_profile(mysql, teams[0].tid)
        return render_template('company_profile.html', company_details=company_details,
                               message=message)
    except Exception as e:
        return render_template('company_profile.html', message=e)
