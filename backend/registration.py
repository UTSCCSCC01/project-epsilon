from flask import Flask, request, render_template
from DAO import DAO

def is_pos_int(s):
    # EP-1: Team management
    try:
        if int(s)>0:
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
            dao.update_role_of_employee(6, 1)
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message)
    else:
        # load if not POST
        return render_template("registration.html")