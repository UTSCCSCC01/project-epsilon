
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from DAO import DAO
from joinTeamRequest import *
from getTeam import getTeam
from removeFromTeam import *
from registration import registration
from userRegistration import user_register
from flask_cors import CORS
from classes.Company import Company
from classes.Request import Request
from classes.Role import Role
from classes.RStatus import RStatus
from classes.Team import Team
from classes.User import User


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
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
        if (request.form['username'] != 'admin' or
                request.form['password'] != 'admin'):
            error = 'Invalid Credentials. Please try again.'
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
    return "Database Users, Teams are deleted!"


@app.route("/create")
def create():
    dao.populate()
    users = dao.get_users()
    teams = dao.get_teams()
    roles = dao.get_roles()
    output = "Database Users, Teams, Roles are populated!\n"

    output += "Also five dummy employees:\n"
    companies = dao.get_companies()
    output = "Database Users, Teams, Roles are populated!</br>"
    output += "Also five dummy employees:</br>"
    for user in users:
        output += str(user) + "\n"
    output += "Also two dummy teams:\n"
        output += str(user) + "</br>"
    output += "Also two dummy teams:</br>"
    for team in teams:
        output += str(team) + "\n"
    output += "Also four roles:\n"
        output += str(team) + "</br>"
    output += "Also three roles:</br>"
    for role in roles:
        output += str(role) + "\n"

        output += str(role.name) + "</br>"
    output += "Also two companies:</br>"
    for company in companies:
        output += str(company.name) +":"+str(company.description)+ "</br>"
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
            dao.remove_team(uid, id2)
            dao.remove_from_team(id2, uid)
        elif op == 'p':
            # newRole should be id of admin
            dao.update_role_of_employee(uid, 2)
            dao.update_role_of_employee(uid, Role.TEAM_ADMIN.value)
        return render_template('displayteam.html')


@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    if data:
        uid = str(data['uid'][0])
        tid = str(data['tid'][0])
        remove_from_team(dao, uid, tid)
        dao.remove_from_team(tid, uid)
        return "Success"
    return "Invalid uid/tid"


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    return getTeam(tid, dao)
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

@app.route('/userRegistration', methods=['GET', 'POST'])
def user_reg():
    return user_register(dao)

# Only go to this page after you go to /create to add more tables and add key constraints

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
        data = team_request_load(dao, action[2])
        return render_template("jointeamrequest.html", message=message, data=data, tid=action[2])
    else:
        # load if not POST
        data = team_request_load(dao, tid)
        if not data:
            return render_template("jointeamrequest.html", message="No pending requests!")
        return render_template("jointeamrequest.html", data=data, tid=tid)
    requests = dao.get_pending_requests(tid)
    data = []
    if not requests:
        return render_template("jointeamrequest.html", message="No pending requests!")
    for req in requests:
        data.append([req.uid, req.create_date, req.req_id])
    return render_template("jointeamrequest.html", data=data, tid=tid, message=message)

@app.route('/userRegistration', methods=['GET', 'POST'])
def user_reg():
    return user_register(dao)

if __name__ == "__main__":
    app.run(debug=True)
