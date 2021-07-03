from modules.UserModule import update_user
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from databaseAccess.DAO import DAO
from joinTeamRequest import *
from registration import registration
from userRegistration import user_register
from search import *

from flask_cors import CORS
from classes.Company import Company
from classes.Request import Request
from classes.Role import Role
from classes.RStatus import RStatus
from classes.Team import Team
from classes.User import User

import mimetypes


mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')


app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'epsilon'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'epsilon_db'

mysql = MySQL(app)
dao = DAO(mysql)


@app.route("/", methods=['GET', 'POST'])
def hello():
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        # if (request.form['username'] != 'admin' or
        #         request.form['password'] != 'admin'):
        #     error = 'Invalid Credentials. Please try again.'
        inp_username = request.form['username']
        inp_password = request.form['password']
        user = dao.get_user_by_contact(inp_username)
        if (not user):
            error = "The email does not exist in our record."
        elif user.password != inp_password:
            error = "Password does not match."
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)


@app.route("/previousHome", methods=['GET', 'POST'])
def previousHome():
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/previousHome')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('previousHome.html')



# Only go to this page if your database is empty

@app.route("/deleteAll")
def delete_all():
    dao.delete_all()
    return "all tables are deleted!"


@app.route("/create")
def create():
    dao.populate()
    users = dao.get_users()
    teams = dao.get_teams()
    roles = dao.get_roles()
    companies = dao.get_companies()
    output = "Database Users, Teams, Roles are populated!</br>"

    output += "Also five dummy employees:</br>"
    for user in users:
        output += str(user) + "</br>"
    output += "Also two dummy teams:</br>"
    for team in teams:
        output += str(team) + "</br>"
    output += "Also three roles:</br>"
    for role in roles:
        output += str(role.name) + "</br>"
    output += "Also two companies:</br>"
    for company in companies:
        output += str(company.name) + ":"+str(company.description) + "</br>"

    return output


# EP-1: Team management
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    return registration(dao)


# result is returned correctly, just need todispaly

# EP-2/4/5
@app.route('/testbtn', methods=['POST'])
def testbtn():
    if request.method == 'POST':
        # id2 is either tid or rid
        op, uid, id2 = request.form['submit'].split(".")
        if op == 'r':
            dao.remove_from_team(id2, uid)
        elif op == 'p':
            # newRole should be id of admin
            dao.update_role_of_employee(uid, Role.TEAM_ADMIN.value)
        return render_template('displayteam.html')


@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    if data:
        uid = str(data['uid'][0])
        tid = str(data['tid'][0])
        dao.remove_from_team(tid, uid)
        return "Success"
    return "Invalid uid/tid"


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    users = dao.get_users_from_team(tid)
    if users:  # there are values in the database
        userDetails = []
        for user in users:
            role = dao.get_role(user.rid)
            userDetails.append([user.name, role.name, user.contact,
                                user.uid, tid, user.rid, user.password])

        return render_template('displayteam.html', userDetails=userDetails)
    else:
        message = "Your team does not exist"
        return render_template('displayteam.html', message=message)


@app.route('/test_get_base_url')
def index():
    return request.base_url[:request.base_url.rfind('/')]


# Only go to this page after you go to /create to add more tables and add key constraints 
@app.route('/testReact', methods=['GET'])
def testReact():
    return {"title": "I am ready from app.py"}


# EP-3: Accept and Decline pending requests

@app.route('/jointeamrequest/<int:tid>/', methods=['GET', 'POST'])
def show_team_request(tid):
    message = ""
    if request.method == 'POST':
        action = request.form["action"].split("_")
        if action[0] == "A":
            message = team_request_accept(dao, action[1])
        elif action[0] == "D":
            message = team_request_decline(dao, action[1])
    requests = dao.get_pending_requests(tid)
    company = dao.get_company_by_id(tid)
    data = []
    if not company:
        return render_template("jointeamrequest.html",
                               message="Your team does not exist.")
    company_name = company.name
    if not requests:
        return render_template("jointeamrequest.html",
                               message="No pending requests!",
                               company_name=company_name)
    for req in requests:
        data.append([req.uid, req.create_date, req.req_id])
    return render_template("jointeamrequest.html", data=data, tid=tid,
                           message=message, company_name=company_name)


# EP-20: Display user profile

@app.route('/user/<int:uid>/', methods=['GET', 'POST'])
def display_user(uid):
    message = ""
    if request.method == 'POST':
        data = request.get_json
        if data:
            message = update_user(dao, uid, request.form["name"],
                                  request.form["description"],
                                  request.form["contact"])
    user = dao.get_user(uid)
    if user:
        user_role = Role(user.rid)
        user_details = [user.name, user.description, user.contact, user_role.name]
        return render_template('userprofile.html', user_details=user_details, message= message)
    else:
        message = "The user does not exist"
        return render_template("userprofile.html", message=message)

# this version of search
@app.route('/search', methods=['GET', 'POST'])
def srch():
    return search(dao)

# related to frontend testing, won't interfere with back end
@app.route('/searchTestSucceed', methods=['GET', 'POST'])
def srch_test_succeed():
    return search_frontend_test(dao, True)


@app.route('/searchTestFail', methods=['GET', 'POST'])
def srch_test_fail():
    return search_frontend_test(dao, False)

@app.route('/userRegistration', methods=['GET', 'POST'])
def user_reg():
    return user_register(dao)

if __name__ == "__main__":
    app.run(debug=True)
