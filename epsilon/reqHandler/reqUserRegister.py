from epsilonModules.ModUser import user_registration
from flask import Flask, request, render_template
from flask_mysqldb import MySQL


def render_user_registration(mysql: MySQL):
    '''
    Registers a User into the database
    :param mysql: database to access
    :return: rendered template of the user registration page
    '''
    if request.method == "POST":
        try:
            email = request.form['username']
            pwd = request.form['password']
            name = request.form['name']
            u_type = None
            if ('type' in request.form):
                u_type = request.form['type']
            message = user_registration(mysql, name, email, pwd, u_type)
            return render_template('user_registration.html', msg=message)
        except Exception as e:
            return render_template('user_registration.html', error=e)
    else:
        return render_template('user_registration.html')
