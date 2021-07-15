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
        return render_template('display_team.html', userDetails=user_details)
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


def render_send_join_team_message(mysql: MySQL):
    """
    """
    if request.method == 'POST':
        print("!!!!!!!!!! entering POST")
        try:
            print("before getting tid ")
            tid = request.form['search']
            print("tid is ", tid)
            uid = current_user.uid
            print("uid is ", uid)
            type_id = current_user.type_id
            print(type(type_id))
            print("type_id is ", type_id)

            if type_id == Type.STARTUP_USER.value:
                message = add_join_team_request(mysql, tid, uid)
                return render_template('send_join_request.html', message=message)
            else:
                if type_id == Type.SERVICE_PROVIDER.value:
                    error = "a service provider cannot request to join a company."
                elif type_id == Type.ADMIN.value:
                    error = "an admin can only process requests, not to send request."
                else:
                    error = "you are not currently registered as any user type, please register as startup user and try again."
                return render_template('send_join_request.html', error=error)
        except Exception as e:
            traceback.print_exc()
            return render_template('send_join_request.html', error=e)
    else:
        print("!!!!!!!!!! entering GET")
        return render_template("send_join_request.html")
