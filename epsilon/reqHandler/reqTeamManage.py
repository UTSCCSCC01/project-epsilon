from epsilonModules.ModTeam import *
from epsilonModules.ModTeamCode import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Type import Type
from classes.TeamCode import TeamCode
from reqHandler.reqCompanyManage import render_company_profile
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
        # action -> (request wanted, uid, tid, rid)
        if action[0] == 'P':
            message = promote_admin(mysql, action[2], action[1], action[3])
        elif action[0] == 'R':
            message = remove_from_team(mysql, action[2], action[1], action[3])
        # action -> (request wanted, tid)
        elif action[0] == 'G':
            message = generateTeamCode(mysql, action[1])
        elif action[0] == 'U':
            message = removeTeamCode(mysql, action[1])
    try:
        teams = get_user_teams(mysql, current_user.uid)
        tid = teams[0].tid
        print(tid)
        cur_role = teams[0].rid
        user_details = get_members(mysql, tid)
        teamCode = getTeamCode(mysql,tid)
        if (teamCode != None):
            code = teamCode.code
            return render_template("team_management_combined.html", tid=tid,
                                message=message, userDetails=user_details, cur_role=cur_role, code=code)
        return render_template("team_management_combined.html", tid=tid,
                               message=message, userDetails=user_details, cur_role=cur_role)
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


def render_join_by_teamCode(mysql:MySQL):
    """
    Handler for join team by entering code
    :param mysql: database to be used
    :return: rendered template of code form
    """
    msg = ""
    if request.method == 'POST':
        # see if they are already in a team
        try:
            team = get_user_teams(mysql, current_user.uid)
            msg = "Already in a team"
        # not in a team
        except:
            code = request.form['code']
            tid = get_tid_by_code(mysql, code)
            # team code exists
            if tid != -1:
                msg = add_to_team(mysql, current_user.uid, tid)
                if msg == "Joined Successfully":
                    return render_template(mysql, msg=msg)
            # code doesn't exist
            else: 
                msg = "Invalid Code"
    return render_template("join_team_by_code.html", error=msg)
