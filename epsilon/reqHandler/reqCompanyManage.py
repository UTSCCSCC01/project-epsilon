from epsilonModules.ModCompany import *
from epsilonModules.ModTeam import get_user_role, get_user_teams
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
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            user_team = [user_teams[0].tid,
                         user_teams[0].uid,
                         user_teams[0].rid]
        
        if name == "":
            tid = user_team[0]
            target_tid = tid
            rid = user_teams[0].rid
        else:   # if name is given or current_user is not logged in
            company_details = get_company_profile_by_name(mysql, name)
            target_tid = company_details.tid
            tid = user_team[0]
            if current_user.is_authenticated:
                rid = get_user_role(mysql, tid, current_user.uid)

        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                message = update_company(mysql, target_tid, name,
                                         description)
        company_details = get_company_profile(mysql, target_tid)
        company_owner = get_company_owner_by_tid(mysql, target_tid)
        if rid in [Role.TEAM_ADMIN.value, Role.TEAM_OWNER.value]:
            return render_template('company_profile.html', company_details=company_details,
                                   message=message, user_team=user_team, tid=tid,
                                   btnName="manage job postings", btnLk="/jobPostingsMgmt",
                                   company_owner=company_owner, target_tid=target_tid)

        return render_template('company_profile.html', company_details=company_details,
                               message=message, user_team=user_team, tid=tid,
                               btnName="view job postings", btnLk="/jobPostings/"+str(tid)+"/",
                               company_owner=company_owner)
    except Exception as e:
        traceback.print_exc()
        return render_template('company_profile.html', error=e)
