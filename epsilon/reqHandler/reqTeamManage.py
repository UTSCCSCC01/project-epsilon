from modules.ModTeam import *
from modules.ModTeam import promote_admin, remove_from_team
from flask import request, render_template, redirect, url_for


def act_on_employee(mysql):
    if request.method == 'POST':
        # id2 is either tid or rid
        op, uid, tid, rid = request.form['submit'].split(".")
        if op == 'r':
            remove_from_team(mysql, tid, uid, rid)
        elif op == 'p':
            promote_admin(mysql, tid, uid, rid)
    return redirect(url_for('displayteam', tid=tid))


def render_display_team(mysql, tid):
    try:
        user_details = get_members(mysql, tid)
        return render_template('displayteam.html', userDetails=user_details)
    except Exception as e:
        return render_template('displayteam.html', message=e)


def render_join_team_request(mysql, tid):
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        if action[0] == "A":
            message = team_request_accept(mysql, action[1])
        elif action[0] == "D":
            message = team_request_decline(mysql, action[1])
    try:
        data, company_name = get_join_requests(mysql, tid)
        if len(data) == 0:
            return render_template("jointeamrequest.html",
                                   message="No pending requests!", tid=tid,
                                   company_name=company_name)
        return render_template("jointeamrequest.html", data=data, tid=tid,
                               message=message, company_name=company_name)
    except Exception as e:
        return render_template("jointeamrequest.html", tid=tid,
                               message=e)
