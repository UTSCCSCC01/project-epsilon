from epsilonModules.ModUser import user_login
from flask import request, render_template, redirect, url_for
from flask_login import current_user, login_user
from werkzeug.urls import url_parse


def render_login(mysql):
    # Return the user to the homepage if they are already logged in
    if current_user.is_authenticated:
        return redirect(url_for('hello'))

    error = None
    if request.method == 'POST':
        # if (request.form['username'] != 'admin' or
        #         request.form['password'] != 'admin'):
        #     error = 'Invalid Credentials. Please try again.'
        inp_username = request.form['E-mail']
        inp_password = request.form['password']
        try:
            user = user_login(mysql, inp_username, inp_password)
            login_user(user)
            # Return to the home page if did not acess restricted
            # page as guest
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('hello')
            return redirect(next_page)
        except Exception as e:
            return render_template('login.html', error=e)
    return render_template('login.html', error=error)
