from modules.ModTeam import get_members
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from modules.ModTeam import promote_admin, remove_from_team
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL


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
    user_details = get_members(mysql, tid)
    if user_details:
        return render_template('displayteam.html', userDetails=user_details)
    else:
        message = "Your team does not exist"
        return render_template('displayteam.html', message=message)
