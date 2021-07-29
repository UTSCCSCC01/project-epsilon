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
    if current_user.is_authenticated:
        user_teams = get_user_teams(mysql, current_user.uid)
        tid = user_teams[0].tid
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


# related to testing frontend, won't interfere with back end
def generate_error_data():
    x = {
        "message": "sample error message"
    }
    return json.dumps(x)


def generate_search_result():
    x = {
        "company_list": [
            {
                "name": "epsilon",
                "description": "sample description of epsilon"
            },

            {
                "name": "delta",
                "description": "sample description of delta"
            },
            {
                "name": "alpha",
                "description": "sample description of alpha"
            }
        ]
    }
    # return x
    return json.dumps(x)


def search_frontend_test(succeed=True):
    print("search_frontend_test")
    if request.method == 'POST':
        if succeed:
            return render_template("search_page.html",
                                   data=generate_search_result())
        else:
            return render_template("search_page.html",
                                   error=generate_error_data())
    else:
        return render_template("search_page.html")
