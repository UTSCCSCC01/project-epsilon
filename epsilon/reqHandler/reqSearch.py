from epsilonModules.ModTeam import get_user_teams
from flask_mysqldb import MySQL
from epsilonModules.ModSearch import company_search
import json
from flask import request, render_template
from flask_login import current_user


def render_company_search(mysql: MySQL):
    """
    Handler for searching a company.
    :param mysql: mysql db.
    :return template for search test
    """
    tid = -1
    try:
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
    except Exception as e:
        tid = -1

    if request.method == 'POST':
        try:
            print("before getting search")
            search = request.form['search']
            print("search is", search)
            data, message = company_search(mysql, search)
            return render_template('search_page.html', message=message,
                                   data=data, tid=tid)
        except Exception as e:
            error_json = json.dumps({"message": str(e)})
            return render_template('search_page.html', error=error_json, tid=tid)
    else:
        return render_template("search_page.html", tid=tid)
        