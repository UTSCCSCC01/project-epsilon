from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from flask_login import current_user

from classes.Type import Type
from epsilonModules.ModService import *
from epsilonModules.ModUser import get_user_by_uid


def render_resources(mysql: MySQL):
    """
    Render the Resources page.
    :return: the template for Resources.
    """
    try:
        global baseUrl
        baseUrl = request.base_url[:request.base_url.rfind('/aboutUs/')]
        tid = -1
        if current_user.is_authenticated and current_user.type_id == Type.STARTUP_USER.value:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
            uid = current_user.uid
            user = get_user_by_uid(mysql, uid)
            if user.type_id == Type.SERVICE_PROVIDER.value or user.type_id == Type.ADMIN.value:
                tid = -1
        return render_template('resources.html', current_user=current_user, tid=tid)
    except Exception as e:
        tid = 0
        return render_template('resources.html',  current_user=current_user, tid=tid)
