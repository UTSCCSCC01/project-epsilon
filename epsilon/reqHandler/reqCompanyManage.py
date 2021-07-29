from epsilonModules.ModCompany import *
from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template
from flask_login import current_user
from classes.Role import Role
import traceback

def render_company_profile(mysql: MySQL, name:str=""):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :param tid: tid of company
    :return template for company profile page.
    """
    message = ""
    try:
        rid = None
        user_team = [0, 0, 0]
        # if name is not given, (endpoint is /yourcompany)
        # we need the user to belong to a company to determine
        # which company to display
        if name == "" and current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            user_team = [user_teams[0].tid,
                         user_teams[0].uid,
                         user_teams[0].rid]
            tid = user_team[0]
            rid = user_team[2]
        else:   # if name is given or current_user is not logged in
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

        if rid in [Role.TEAM_ADMIN.value, Role.TEAM_OWNER.value]:
            return render_template('company_profile.html', company_details=company_details,
                                   message=message, user_team=user_team, tid=tid,
                                   btnName="manage job postings", btnLk="/jobPostingsMgmt")

        # if displayJobPostingMgmt=False, only display the job postings w/o management option
        return render_template('company_profile.html', company_details=company_details,
                               message=message, user_team=user_team, tid=tid,
                               btnName="view job postings", btnLk="/jobPostings/"+str(tid)+"/")
    except Exception as e:
        traceback.print_exc()
        return render_template('company_profile.html', error=e)
