from modules.ModUser import user_login
from flask import request, render_template, redirect, url_for


def render_login(mysql):
    error = None
    if request.method == 'POST':
        # if (request.form['username'] != 'admin' or
        #         request.form['password'] != 'admin'):
        #     error = 'Invalid Credentials. Please try again.'
        inp_username = request.form['username']
        inp_password = request.form['password']
        try:
            user = user_login(mysql, inp_username, inp_password)
            return redirect(url_for('hello'))
        except Exception as e:
            return render_template('login.html', error=e)
    return render_template('login.html', error=error)
