from flask import request, render_template, redirect, url_for
from flask_login import current_user
from flask_mysqldb import MySQL
from epsilonModules.ModTeam import get_user_teams


def render_home(mysql: MySQL):
    """
    Render the home page.
    :return: the template for home page.
    """
    try:
        global baseUrl
        baseUrl = request.base_url[:request.base_url.rfind('/')]
        tid = -1
        if request.method == 'POST':
            return redirect(url_for('login'))

        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('home.html', tid=tid)
    except Exception as e:
        return render_template('home.html', tid=tid)


def render_previous_home():
    """
    Render the old version of home page.
    :return: the template for previous home page.
    """
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/previousHome')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('previous_home.html')
