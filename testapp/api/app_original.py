from reqHandler.reqCompanyManage import render_company_profile
from reqHandler.reqSearch import render_company_search, search_frontend_test
from reqHandler.reqUserManage import render_user_profile
from reqHandler.reqUserRegister import render_user_registration
from reqHandler.reqTeamManage import *
from reqHandler.reqTeamRegister import render_team_registration
from reqHandler.reqLogin import render_login
from reqHandler.reqDatabaseManage import create_tables, delete_tables
from reqHandler.reqHome import *
from flask import Flask, request
from flask_mysqldb import MySQL
from flask_cors import CORS

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


# For front end test? If you are sure it's not used please delete.
@app.route('/test_get_base_url')
def index():
    return request.base_url[:request.base_url.rfind('/')]


@app.route('/testReact', methods=['GET'])
def testReact():
    return {"title": "I am ready from app.py"}


# EP-1: Team management
@app.route('/registration', methods=['GET', 'POST'])
def reg():
    return render_team_registration(mysql)


# EP-2/4/5
@app.route('/testbtn/', methods=['POST'])
def testbtn():
    return act_on_employee(mysql)


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def displayteam(tid):
    return render_display_team(mysql, tid)


# EP-3: Accept and Decline pending requests
@app.route('/jointeamrequest/<int:tid>/', methods=['GET', 'POST'])
def show_team_request(tid):
    return render_join_team_request(mysql, tid)


# EP-20: Display user profile
@app.route('/user/<int:uid>/', methods=['GET', 'POST'])
def display_user(uid):
    return render_user_profile(mysql, uid)


# this version of search
@app.route('/search', methods=['GET', 'POST'])
def srch():
    return render_company_search(mysql)


# related to frontend testing, won't interfere with back end
@app.route('/searchTestSucceed', methods=['GET', 'POST'])
def srch_test_succeed():
    return search_frontend_test(True)


@app.route('/searchTestFail', methods=['GET', 'POST'])
def srch_test_fail():
    return search_frontend_test(False)


@app.route('/userRegistration', methods=['GET', 'POST'])
def user_reg():
    return render_user_registration(mysql)


# EP-69: Display company profile
@app.route('/company/<int:tid>/', methods=['GET', 'POST'])
def display_company(tid):
    return render_company_profile(mysql, tid)


if __name__ == "__main__":
    app.run(debug=True)
