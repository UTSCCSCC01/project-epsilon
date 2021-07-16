from flask_mysqldb import MySQL
from epsilon.epsilonModules.ModSearch import company_search
import json
from flask import request, render_template


def render_company_search(mysql: MySQL):
    """
    Handler for searching a company.
    :param mysql: mysql db.
    :return template for search test
    """
    if request.method == 'POST':
        try:
            search = request.form['search']
            data, message = company_search(mysql, search)
            return render_template('search_page.html', message=message,
                                   data=data)
        except Exception as e:
            error_json = json.dumps({"message": str(e)})
            return render_template('search_page.html', error=error_json)
    else:
        return render_template("search_page.html")


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
