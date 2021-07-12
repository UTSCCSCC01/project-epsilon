from epsilonModules.ModCompany import *
from flask import request, render_template, redirect, url_for


def render_company_profile(mysql: MySQL, tid: int):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :param tid: tid of company
    :return template for company profile page.
    """
    message = ""
    try:
        if request.method == 'POST':
            data = request.get_json
            if data:
                name = request.form["name"]
                description = request.form["description"]
                message = update_company(mysql, tid, name,
                                         description)
        company_details = get_company_profile(mysql, tid)
        return render_template('company_profile.html', company_details=company_details,
                               message=message)
    except Exception as e:
        return render_template('company_profile.html', message=e)
