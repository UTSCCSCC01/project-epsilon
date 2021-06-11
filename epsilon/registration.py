from flask import Flask, request, render_template
from populatedatabase import add_data, get_data

def is_pos_int(s):
    # EP-1: Team management
    try:
        if int(s)>0:
            return True
        else:
            return False
    except ValueError:
        return False

def check_team_exists(mysql, name):
    # Returns 1 if match is found else returns 0
    companies = get_data(mysql, "Company")
    for item in companies:
        if (item[1].lower() == name.lower()):
            return 1
    return 0

def registration(mysql):
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
        if (check_team_exists(mysql, request.form['teamname']) == 1):
            error = 'This company already exists. Please try with a new name or request to join ' + request.form['teamname'] + ' here.'
            return render_template('registration.html', error=error)
        # if no errors
        try:
            message = add_data(
                mysql, sql_q, (request.form['teamname'], request.form['teamdesc']))
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message)
    else:
        # load if not POST
        return render_template("registration.html")