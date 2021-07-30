
from epsilonModules.ModCompany import get_company_profile
import json
from epsilonModules.ModTeam import *
from epsilonModules.ModTeamCode import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Type import Type
from classes.TeamCode import TeamCode
from classes.Role import Role
import sys, traceback


def render_team_mgmt_combined(mysql: MySQL):
    """
    Handler for page containing both join 
    team request and team management
    :param: mysql: mysql db
    :return: template for combined page
    """
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        # action -> (request wanted, jap_id, tid)
        if action[0] == 'I':
            message = update_jap_to_rstatus(mysql, action[1], RStatus.INTERVIEW)
        elif action[0] == 'O':
            message = update_jap_to_rstatus(mysql, action[1], RStatus.OFFER)
        elif action[0] == 'D':
            message = update_jap_to_rstatus(mysql, action[1], RStatus.REJECTED)
        # action -> (request wanted, uid, tid, rid)
        elif action[0] == 'P':
            message = promote_admin(mysql, action[2], action[1], action[3])
        elif action[0] == 'R':
            message = remove_from_team(mysql, action[2], action[1], action[3])
        elif action[0] == 'G':
            message = generateTeamCode(mysql, action[1])
        elif action[0] == 'U':
            message = removeTeamCode(mysql, action[1])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        cur_role = teams[0].rid
        # data, company_name = get_join_requests(mysql, tid)
        company_name = get_company_profile(mysql, tid)[0]
        user_details = get_members(mysql, tid)
        applicant_details = get_applicant_details(mysql, tid)
        teamCode = getTeamCode(mysql,tid)
        if (teamCode != None):
            code = teamCode.code
            if len(applicant_details) == 0:
                return render_template("team_management_combined.html",
                                    applicant_message="No applicants!", tid=tid,
                                    company_name=company_name, userDetails=
                                    user_details, cur_role=cur_role, code=code,
                                    message=message)
            return render_template("team_management_combined.html", applicant_details = applicant_details,
                                tid=tid, message=message, company_name=company_name, 
                                userDetails=user_details, cur_role=cur_role, code=code)
        if len(applicant_details) == 0:
                return render_template("team_management_combined.html",
                                    applicant_message="No applicants!", tid=tid,
                                    company_name=company_name, userDetails=
                                    user_details, cur_role=cur_role,
                                    message=message)
        return render_template("team_management_combined.html", applicant_details=applicant_details,
                                tid=tid, message=message, company_name=company_name, 
                                userDetails=user_details, cur_role=cur_role)                        
    except Exception as e:
        return render_template("team_management_combined.html",
                               message=e)


def render_send_join_team_message(mysql: MySQL, by_tid: bool):
    """
    Handler for sending join team request.
    :param mysql: mysql db.
    :return template for sending join team request.
    """
    template_choice_dict = {True: "company ID", False: "company name"}
    if request.method == "POST":
        try:
            uid = current_user.uid
            type_id = current_user.type_id
            if by_tid:
                tid = str(request.form["search"])
                message = add_join_team_request_by_tid(mysql=mysql, tid=tid,
                                                       uid=uid, type_id=type_id)

            else:
                company_name = request.form["search"]
                message = add_join_team_request_by_company_name(mysql=mysql,
                                                                company_name=company_name, uid=uid, type_id=type_id)
            return render_template("send_join_request.html",
                                   choice=template_choice_dict[by_tid],
                                   message=message)
        except ValueError as ve:
            return render_template("send_join_request.html", error="company id is digit format",
                                   choice=template_choice_dict[by_tid])
        except Exception as e:
            traceback.print_exc()
            return render_template("send_join_request.html", error=e,
                                   choice=template_choice_dict[by_tid])
    else:
        return render_template("send_join_request.html",
                               choice=template_choice_dict[by_tid])


def render_choose_how_to_send_join_request():
    """
    Handler for choose how to send join team request.
    """
    return render_template("choose_how_to_send_join_request.html")
