from flask_mysqldb import MySQL
from epsilon.modules.ModCompany import register_team
from databaseAccess.DAOIndustry import DAOIndustry
from flask import request, render_template


def render_team_registration(mysql: MySQL):
    """
    Renders the template for team registration.
    :param mysql: mysql db.
    :return Renders the template for team registration.
    """
    dao_industry = DAOIndustry(mysql)
    industry = dao_industry.get_industries()
    if request.method == 'POST':
        name = request.form['teamname']
        desc = request.form['teamdesc']
        indust = request.form['industryselect']
        try:
            message = register_team(mysql, name, desc, indust)
            return render_template("registration.html", message=message,
                                   industry=industry)
        except Exception as e:
            return render_template("registration.html", error=e,
                                   industry=industry)
    else:
        # load if not POST
        return render_template("registration.html", industry=industry)
