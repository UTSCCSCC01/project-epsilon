import json
from epsilonModules.ModTeam import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Type import Type
import sys, traceback

def act_on_employee(mysql: MySQL):
    """
    Handler for delete/promot an employee in team.
    :param mysql: mysql db.
    :return redirect to display_team
    """
    if request.method == 'POST':
        # id2 is either tid or rid
        op, uid, tid, rid = request.form['submit'].split(".")
        if op == 'r':
            remove_from_team(mysql, tid, uid, rid)
        elif op == 'p':
            promote_admin(mysql, tid, uid, rid)
    return redirect(url_for('displayteam', tid=tid))


def render_display_team(mysql: MySQL):
    """
    Handler for displaying team members in a team.
    :param mysql: mysql db.
    :param tid: tid of team.
    :return template for display team.
    """
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        user_details = get_members(mysql, tid)
        return render_template('display_team.html', userDetails=user_details, tid=tid)
    except Exception as e:
        return render_template('display_team.html', message=e)


def render_join_team_request(mysql: MySQL):
    """
    Handler for join team request.
    :param mysql: mysql db.
    :param tid: tid of team.
    :return template for join team request.
    """
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        if action[0] == "A":
            message = team_request_accept(mysql, action[1])
        elif action[0] == "D":
            message = team_request_decline(mysql, action[1])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        data, company_name = get_join_requests(mysql, tid)
        if len(data) == 0:
            return render_template("join_team_request.html",
                                   message="No pending requests!", tid=tid,
                                   company_name=company_name)
        return render_template("join_team_request.html", data=data, tid=tid,
                               message=message, company_name=company_name)
    except Exception as e:
        return render_template("join_team_request.html",
                               message=e)

      
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
        # action -> (request wanted, req id, tid)
        if action[0] == 'A':
            message = team_request_accept(mysql, action[1])
        elif action[0] == 'D':
            message = team_request_decline(mysql, action[1])
        # action -> (request wanted, uid, tid, rid)
        elif action[0] == 'P':
            message = promote_admin(mysql, action[2], action[1], action[3])
        elif action[0] == 'R':
            message = remove_from_team(mysql, action[2], action[1], action[3])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        cur_role = teams[0].rid
        data, company_name = get_join_requests(mysql, tid)
        user_details = get_members(mysql, tid)
        if len(data) == 0:
            return render_template("team_management_combined.html",
                                   message="No pending requests!", tid=tid,
                                   company_name=company_name, userDetails=
                                   user_details, cur_role=cur_role)
        return render_template("team_management_combined.html", data=data, tid=tid,
                               message=message, company_name=company_name, 
                               userDetails=user_details, cur_role=cur_role)
    except Exception as e:
        return render_template("team_management_combined.html",
                               message=e)


def render_send_join_team_message(mysql: MySQL, by_tid:bool):
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