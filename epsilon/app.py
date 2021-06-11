from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL

from populatedatabase import *
from business import *
from getTeam import getTeam
from removeFromTeam import *
from registration import registration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'epsilon'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'epsilon_db'

mysql = MySQL(app)


@app.route("/")
def hello():
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/')]
    return "Hello World! Welcome to Epsilon!"

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
    cur1 = mysql.connection.cursor()
    cur1.execute('''DROP TABLE IF EXISTS Teams''')
    cur1.execute('''DROP TABLE IF EXISTS Request''')
    cur1.execute('''DROP TABLE IF EXISTS Users''')
    cur1.execute('''DROP TABLE IF EXISTS Roles''')
    cur1.execute('''DROP TABLE IF EXISTS Company''')
    cur1.execute('''DROP TABLE IF EXISTS RStatus''')
    mysql.connection.commit()
    return "Database Users, Teams are deleted!"


@app.route("/create")
def create():

    populate(mysql)
    cur1 = mysql.connection.cursor()
    cur1.execute('''SELECT * FROM Users''')
    cur2 = mysql.connection.cursor()
    cur2.execute('''SELECT * FROM Teams''')
    cur3 = mysql.connection.cursor()
    cur3.execute('''SELECT * FROM Roles''')
    return "Database Users, Teams, Roles are populated!\n" \
           "Also five dummy employees Paula, Tim, Pritish, Sam, Water."+"\n\n"\
           + str(cur1.fetchall())+"\n\n"+str(cur2.fetchall())\
           + "\n\n"+str(cur3.fetchall())


# EP-1: Team management
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    return registration(mysql)

# result is returned correctly, just need todispaly

# EP-2/4/5
@app.route('/testbtn', methods=['POST'])
def testbtn():
    if request.method == 'POST':
        # id2 is either tid or rid
        op, uid, id2 = request.form['submit'].split(".")
        if op == 'r':
            removeFromTeam(mysql, uid, id2)
        elif op == 'p':
            # newRole should be id of admin
            updateRoleOfEmployee(mysql,uid,2)
        return render_template('displayteam.html')


@app.route('/remove', methods=['POST'])
def remove():
    cur = mysql.connection.cursor()
    data = request.json
    if data:
        uid = str(data['uid'][0])
        tid = str(data['tid'][0])
        removeFromTeam(uid, tid)
        return "Success"
    return "Invalid uid/tid"


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    return getTeam(tid, mysql)

@app.route('/test_get_base_url')
def index():
    return request.base_url[:request.base_url.rfind('/')]


# Only go to this page after you go to /create to add more tables and add key constraints 

# EP-3: Accept and Decline pending requests

@app.route('/jointeamrequest/<int:tid>/', methods=['GET', 'POST'])
def show_team_request(tid):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        action = request.form["action"].split("_")
        if action[0] == "A":
            message = team_request_accept(mysql, action[1])
        elif action[0] == "D":
            message = team_request_decline(mysql, action[1])
        data = team_request_load(mysql, action[2])
        return render_template("jointeamrequest.html", message=message, data=data, tid = action[2])
    else:
        # load if not POST
        data = team_request_load(mysql, tid)
        if len(data) == 0:
            return render_template("jointeamrequest.html", message="No pending requests!")
        return render_template("jointeamrequest.html", data = data, tid = tid)
      
if __name__ == "__main__":
    app.run(debug=True)
