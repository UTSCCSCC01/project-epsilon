from os import remove
from epsilonModules.ModCompany import *
from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template
from flask_login import current_user
from classes.Role import Role
from epsilonModules.ModCPic import*
import traceback
import os

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
            tid = user_teams[0].tid
            rid = user_teams[0].rid
        else:   # if name is given or current_user is not logged in
            company_details = get_company_profile_by_name(mysql, name)
            tid = company_details.tid

        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                message = update_company(mysql, tid, name,
                                         description)
                if 'pfpi' in request.files:
                    f = request.files['pfpi']
                    if f.filename != '':
                        file = f.stream.read()
                        if get_cpic(mysql,tid) is not None:
                            edit_cpic(mysql,tid,file)
                        else:
                            add_cpic(mysql,tid,file)
        pfp = get_cpic(mysql,tid)
        if pfp:
            if os.path.exists("./static/cpfp.png"):
                os.remove("./static/cpfp.png")
            with open('./static/cpfp.png', 'wb') as wf:
                wf.write(pfp)
        company_details = get_company_profile(mysql, tid)
        company_owner = get_company_owner_by_tid(mysql, tid)
        if rid in [Role.TEAM_ADMIN.value, Role.TEAM_OWNER.value]:
            return render_template('company_profile.html', company_details=company_details,
                                   message=message, user_team=user_team, tid=tid,
                                   btnName="manage job postings", btnLk="/jobPostingsMgmt",
                                   company_owner=company_owner, pic=pfp)

        return render_template('company_profile.html', company_details=company_details,
                               message=message, user_team=user_team, tid=tid,
                               btnName="view job postings", btnLk="/jobPostings/"+str(tid)+"/",
                               company_owner=company_owner, pic=pfp)
    except Exception as e:
        traceback.print_exc()
        print(e)
        return render_template('company_profile.html', error=e)
