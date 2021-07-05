from reqHandler.reqTeamManage import act_on_employee
from reqHandler.reqTeamRegister import render_team_registration
from reqHandler.reqLogin import render_login
from reqHandler.reqDatabaseManage import create_tables, delete_tables
from reqHandler.reqHome import render_previous_home
from reqHandler.reqHome import render_home
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOUser import DAOUser
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from modules.ModUser import update_user
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from databaseAccess.DAO import DAO
from joinTeamRequest import *
from userRegistration import user_register
from modules.search import *

from flask_cors import CORS
from classes.Role import Role
from classes.RStatus import RStatus

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


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_home()


@app.route("/previousHome", methods=['GET', 'POST'])
def previousHome():
    return render_previous_home()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_login(mysql)


# For database management
@app.route("/deleteAll")
def delete_all():
    return delete_tables(mysql)


@app.route("/create")
def create():
    return create_tables(mysql)


# EP-1: Team management
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    return render_team_registration(mysql)


# result is returned correctly, just need todispaly

# EP-2/4/5
@app.route('/testbtn/', methods=['POST'])
def testbtn():
    return act_on_employee(mysql)


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    dao_team = DAOTeam(mysql)
    dao_role = DAORole(mysql)
    users = dao_team.get_users_from_team(tid)
    if users:  # there are values in the database
        userDetails = []
        for user in users:
            role = dao_role.get_role_by_rid(user.rid)
            userDetails.append([user.name, role.name, user.contact,
                                user.uid, tid, user.rid])

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
            message = team_request_accept(mysql, action[1])
        elif action[0] == "D":
            message = team_request_decline(mysql, action[1])
    dao_request = DAORequest(mysql)
    dao_company = DAOCompany(mysql)    
    requests = dao_request.get_requests_by_tid_sid(tid, RStatus.PENDING.value)
    company = dao_company.get_company_by_tid(tid)
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
    dao_user = DAOUser(mysql)
    message = ""
    if request.method == 'POST':
        data = request.get_json
        if data:
            message = update_user(mysql, uid, request.form["name"],
                                  request.form["description"],
                                  request.form["contact"])
    user = dao_user.get_user_by_uid(uid)
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
    return search(mysql)

# related to frontend testing, won't interfere with back end
@app.route('/searchTestSucceed', methods=['GET', 'POST'])
def srch_test_succeed():
    return search_frontend_test(True)


@app.route('/searchTestFail', methods=['GET', 'POST'])
def srch_test_fail():
    return search_frontend_test(False)

@app.route('/userRegistration', methods=['GET', 'POST'])
def user_reg():
    return user_register(mysql)

if __name__ == "__main__":
    app.run(debug=True)
