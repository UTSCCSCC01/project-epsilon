from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from DAO import DAO
from joinTeamRequest import *
from getTeam import getTeam
from removeFromTeam import *
from registration import registration
from flask_cors import CORS
from classes.Company import Company
from classes.Request import Request
from classes.Role import Role
from classes.RStatus import RStatus
from classes.Team import Team
from classes.User import User


app = Flask(__name__)

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

# Only go to this page if your database is empty

@app.route("/deleteAll")
def delete_all():
    dao.delete_all()
    return "Database Users, Teams are deleted!"


@app.route("/create")
def create():

    dao.populate()
    users = dao.get_Users()
    teams = dao.get_Teams()
    roles = dao.get_Roles()
    return "Database Users, Teams, Roles are populated!\n" \
           "Also five dummy employees Paula, Tim, Pritish, Sam, Water."+"\n\n"\
           + str(users)+"\n\n"+str(teams)\
           + "\n\n"+str(roles)


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
            dao.removeTeam(uid, id2)
        elif op == 'p':
            # newRole should be id of admin
            dao.updateRoleOfEmployee(uid,2)
        return render_template('displayteam.html')


@app.route('/remove', methods=['POST'])
def remove():
    data = request.json
    if data:
        uid = str(data['uid'][0])
        tid = str(data['tid'][0])
        removeFromTeam(dao, uid, tid)
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
            userDetails.append([user.name, role.role_type, user.contact,
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


# Only go to this page after you go to /create to add more tables and add
# key constraints

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
        return render_template("jointeamrequest.html", message=message, data=data, tid = action[2])
        requests = dao.get_pending_requests(action[2])
        data = []
        for req in requests:
            data.append([req.uid, req.create_date, req.req_id])
        return render_template(
            "jointeamrequest.html",
            message=message,
            data=data,
            tid=action[2])
    else:
        # load if not POST
        data = team_request_load(dao, tid)
        requests = dao.get_pending_requests(tid)
        data = []
        for req in requests:
            data.append([req.uid, req.create_date, req.req_id])
        if not data:
            return render_template("jointeamrequest.html", message="No pending requests!")
        return render_template("jointeamrequest.html", data = data, tid = tid)
      
            return render_template(
                "jointeamrequest.html",
                message="No pending requests!")
        return render_template("jointeamrequest.html", data=data, tid=tid)


if __name__ == "__main__":
    app.run(debug=True)