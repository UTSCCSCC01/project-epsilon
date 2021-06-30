from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from DAO import DAO
from joinTeamRequest import *
from getTeam import getTeam
from removeFromTeam import *
from registration import registration
from search import search
from flask_cors import CORS
import json

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
    # token is only for testing connection
    return render_template('home.html', token="Hello Flask+React!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)


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
    for user in users:
        output += str(user) + "\n"
    output += "Also two dummy teams:\n"
    for team in teams:
        output += str(team) + "\n"
    output += "Also four roles:\n"
    for role in roles:
        output += str(role) + "\n"

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
        elif op == 'p':
            # newRole should be id of admin
            dao.update_role_of_employee(uid, 2)
        return render_template('displayteam.html')


@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    if data:
        uid = str(data['uid'][0])
        tid = str(data['tid'][0])
        remove_from_team(dao, uid, tid)
        return "Success"
    return "Invalid uid/tid"


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    return getTeam(tid, dao)


@app.route('/test_get_base_url')
def index():
    return request.base_url[:request.base_url.rfind('/')]


@app.route('/testReact', methods=['GET'])
def testReact():
    return {"title": "I am ready from app.py"}


# Only go to this page after you go to /create to add more tables and add key constraints

# EP-3: Accept and Decline pending requests

@app.route('/jointeamrequest/<int:tid>/', methods=['GET', 'POST'])
def show_team_request(tid):
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
        return render_template("jointeamrequest.html", data = data, tid = tid)

# this version of search
@app.route('/search', methods=['GET', 'POST'])
def srch():
    return search(dao)
      
@app.route('/searchTest', methods=['GET', 'POST'])
def srch_test():
    # mock object returned by search(dao)
    x = {
        "name": "my company limited",
        "description": 30
    }
    return json.dumps(x)


if __name__ == "__main__":
    app.run(debug=True)
