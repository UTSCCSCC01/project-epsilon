from classes.Role import Role
from classes.Team import Team
from classes.User import User
from classes.Company import Company
from flask import Flask, request, render_template
from DAO import DAO


def is_pos_int(s):
    # EP-1: Team management
    try:
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def check_team_exists(dao, name):
    # Returns 1 if match is found else returns 0
    companies = dao.get_companies()
    for company in companies:
        if company.name.lower() == name.lower():
            return 1
    return 0


def registration(dao):
    # TODO: check if user is logged in and check permissions
    # cur = mysql.connection.cursor()
    industry = dao.get_industry()
    if request.method == 'POST':
        # check if all form boxes are completed
        if (len(request.form['teamname']) == 0 or len(request.form['teamdesc']) == 0 or len(request.form['industryselect']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('registration.html', error=error, industry=industry)
        # If the company exists.
        if (check_team_exists(dao, request.form['teamname']) == 1):
            error = 'This company already exists. Please try with a new name or request to join ' + request.form['teamname'] + ' here.'
            return render_template('registration.html', error=error, industry=industry)
        # if no errors
        try:
            company = Company(name=request.form['teamname'],
                              description=request.form['teamdesc'],ind_id=request.form['industryselect'])
            dao.add_company(company)
            joe = User(rid=Role.TEAM_OWNER.value, name="Joe", contact="Jo@gmail.com")
            team = Team(tid=3, uid=6, rid=Role.TEAM_OWNER.value)
            dao.add_user(joe)
            dao.add_team(team)
            message = "Registered!"
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message, industry=industry)
    else:
        # load if not POST
        return render_template("registration.html", industry=industry)
