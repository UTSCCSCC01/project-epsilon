from databaseAccess.DAOUser import DAOUser
from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from classes.User import User
import re

# EP-23 User Registration

def user_exists(user_dao: DAOUser, email: str):
    '''
    Checks if the user already exists in the database
    :param user_dao: database access point
    :param email: the email of the user being registered
    :return: whether the email is already in use
    '''
    # get existing users in db
    user = user_dao.get_user_by_contact(email)
    # iterate through users
    if user:
        # check for email match
        if user.contact.lower() == email.lower():
            return True
    # no users remain that may exist already
    return False

def user_register(mysql: MySQL):
    '''
    Registers a User into the database
    :param mysql: database to access
    :return: rendered template of the user registration page
    '''
    if request.method == "POST":
        email = request.form['username']
        pwd = request.form['password']
        name = request.form['name']
        u_type = None
        user_dao = DAOUser(mysql)
        if ('type' in request.form):
            u_type = request.form['type']
        # check if any required fields isn't filled
        if (len(email)==0 or len(pwd)==0 or len(name)==0 or u_type==None):
            e = "Please fill required fields"
            return render_template('userRegistration.html', error = e)
        # check if the user email is already in use (username)
        elif (user_exists(user_dao, email)):
            e = "Email already in use, please use another one"
            return render_template('userRegistration.html', error = e)
        # check email format
        elif (not re.search(".+@{1}.+\..+",email) or len(re.findall("@",email))>1):
            e = "Invalid email"
            return render_template('userRegistration.html', error = e)
        else:
            try:
                # create new user
                user = User(rid=u_type, name=name, contact=email, password=pwd)
                user_dao.add_user(user)
                # send success prompt
                e = "Account successfully created!"
                return render_template('userRegistration.html', msg = e)
            except Exception as e:
                # display issue w db
                return render_template('userRegistration.html', error = e)
    else:
        return render_template('userRegistration.html')
        