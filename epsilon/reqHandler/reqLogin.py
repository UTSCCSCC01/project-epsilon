from databaseAccess.DAOUser import DAOUser
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL


def render_login(mysql):
    error = None
    if request.method == 'POST':
        # if (request.form['username'] != 'admin' or
        #         request.form['password'] != 'admin'):
        #     error = 'Invalid Credentials. Please try again.'
        inp_username = request.form['username']
        inp_password = request.form['password']
        dao_user = DAOUser(mysql)
        user = dao_user.get_user_by_contact(inp_username)
        if (not user):
            error = "The email does not exist in our record."
        elif user.password != inp_password:
            error = "Password does not match."
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)
