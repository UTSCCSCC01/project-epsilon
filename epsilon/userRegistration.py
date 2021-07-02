from flask import Flask, request, render_template
from DAO import DAO
from classes.User import User

# EP-23 User Registration

def user_exists(dao: DAO, user: str):
    '''
    Checks if the user already exists in the database
    :param dao: database access point
    :param user: the email of the user being registered
    :return: whether the email is already in use
    '''
    # get existing users in db
    users = dao.get_users()
    # iterate through users
    for u in users:
        # check for email match
        if u._contact.lower() == user.lower():
            return True
    # no users remain that may exist already
    return False

def user_register(dao: DAO):
    '''
    Registers a User into the database
    :param dao: database to access
    :return: rendered template of the user registration page
    '''
    if request.method == "POST":
        email = request.form['username']
        pwd = request.form['password']
        name = request.form['name']
        u_type = None
        if ('type' in request.form):
            u_type = request.form['type']
        # check if any required fields isn't filled
        if (len(email)==0 or len(pwd)==0 or len(name)==0 or u_type==None):
            e = "Please fill required fields"
            return render_template('userRegistration.html', error = e)
        # check if the user email is already in use (username)
        elif (user_exists(dao,email)):
            e = "Email already in use, please use another one"
            return render_template('userRegistration.html', error = e)
        else:
            try:
                # retrieve next available uid
                query = "SELECT max(uid) FROM Users"
                temp = dao.get_data(query,None)
                uid =  temp[0][0] + 1
                # create new user
                user = User(uid,u_type,name,email,pwd)
                print(user)
                dao.add_user(user)
                
                # send success prompt
                e = "Account successfully created!"
                return render_template('userRegistration.html', msg = e)
            except Exception as e:
                # display issue w db
                return render_template('userRegistration.html', error = e)
    else:
        return render_template('userRegistration.html')
        