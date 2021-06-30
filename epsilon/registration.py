from classes.Team import Team
from classes.User import User
from classes.Company import Company
from flask import Flask, request, render_template
from DAO import DAO


def is_pos_int(s):
    # EP-1: Team management
    try:
        if int(s)>0:
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def check_team_exists(dao, name):
    # Returns 1 if match is found else returns 0
    companies = dao.get_Companies()
    for item in companies:
        if (item[1].lower() == name.lower()):
            return 1
    return 0


def registration(dao):
    # TODO: check if user is logged in and check permissions
    # cur = mysql.connection.cursor()
    if request.method == 'POST':
        # create both queries for checking and inserting data
        sql_q = '''INSERT INTO Company (name, description) VALUES (%s, %s)'''
        # check if all form boxes are completed
        if (len(request.form['teamname']) == 0 or len(request.form['teamdesc']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('registration.html', error=error)
        # If the company exists.
        if (check_team_exists(dao, request.form['teamname']) == 1):
            error = 'This company already exists. Please try with a new name or request to join ' + request.form['teamname'] + ' here.'
            return render_template('registration.html', error=error)
        # if no errors
        try:
            message = dao.modify_data(
                sql_q, (request.form['teamname'], request.form['teamdesc']))
            dao.modify_data('''INSERT INTO Users (uid, rid, name, contact) VALUES (%s, %s, %s, %s)''', (6, 0, "Joe", "Jo@gmail.com"))
            dao.modify_data('''INSERT INTO Teams (tid, uid, role) VALUES (%s, %s, %s)''', (3, 6, 1))
            dao.updateRoleOfEmployee(6, 1)
            company = Company(name=request.form['teamname'],
                              description=request.form['teamdesc'])
            message = dao.add_company(company)
            joe = User(rid=1, name="Joe", contact="Jo@gmail.com")
            team = Team(tid=3, uid=6, rid=1)
            dao.add_user(joe)
            dao.add_team(team)
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message)
    else:
        # load if not POST
        return render_template("registration.html")        return render_template("registration.html")
        return render_template("registration.html")
