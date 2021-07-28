from flask_mysqldb import MySQL
from epsilonModules.ModSearch import company_search
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
            print("before getting search")
            search = request.form['search']
            print("search is", search)
            data, message = company_search(mysql, search)
            return render_template('search_page.html', message=message,
                                   data=data)
        except Exception as e:
            error_json = json.dumps({"message": str(e)})
            return render_template('search_page.html', error=error_json)
    else:
        return render_template("search_page.html")
