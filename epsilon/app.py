from reqHandler.reqCompanyManage import render_company_profile
from reqHandler.reqUserManage import load_User_O, render_user_profile
from reqHandler.reqUserRegister import render_user_registration
from reqHandler.reqAboutUs import render_about_us
from reqHandler.reqTeamManage import *
from reqHandler.reqTeamRegister import render_team_registration
from reqHandler.reqLogin import render_login
from reqHandler.reqLogout import render_logout
from reqHandler.reqDatabaseManage import create_tables, delete_tables
from reqHandler.reqHome import *
from reqHandler.reqJobPosting import *
from flask import Flask, request
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_required
from flask_cors import CORS
from databaseAccess.DAOUser import *

app = Flask(__name__)
CORS(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'epsilon'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'epsilon_db'
app.config['SECRET_KEY'] = 'henlo'

mysql = MySQL(app)


@app.route("/", methods=['GET', 'POST'])
def hello():
    return render_home()


@app.route("/previousHome/", methods=['GET', 'POST'])
def previousHome():
    return render_previous_home()


@app.route('/login/', methods=['GET', 'POST'])
def login():
    return render_login(mysql)


# For database management
@app.route("/deleteAll/")
def delete_all():
    return delete_tables(mysql)


@app.route("/create/")
def create():
    return create_tables(mysql)

# EP-1: Team management
@app.route('/registration/', methods=['GET', 'POST'])
@login_required
def reg():
    return render_team_registration(mysql)


# EP-2/4/5
@app.route('/testbtn/', methods=['POST'])
@login_required
def testbtn():
    return act_on_employee(mysql)


@app.route("/displayteam/", methods=['GET'])
@login_required
def displayteam():
    return render_display_team(mysql)


# EP-3: Accept and Decline pending requests
@app.route('/jointeamrequest/', methods=['GET', 'POST'])
@login_required
def show_team_request():
    return render_join_team_request(mysql)


# EP-20: Display user profile
@app.route('/user/', methods=['GET', 'POST'])
@login_required
def display_user():
    return render_user_profile(mysql)


# this version of search
@app.route('/search/', methods=['GET', 'POST'])
def srch():
    return render_company_search(mysql)

@app.route('/userRegistration/', methods=['GET', 'POST'])
def user_reg():
    return render_user_registration(mysql)


@app.route('/aboutUs/', methods=['GET', 'POST'])
def about():
    return render_about_us()


# EP-69: Display company profile
@app.route('/company/', methods=['GET', 'POST'])
@login_required
def display_company():
    return render_company_profile(mysql)


@app.route('/logout/')
@login_required
def logout():
    return render_logout()


#E EP-73 
@app.route('/teamManagement/', methods=['GET', 'POST'])
@login_required
def teamMgmt():
    return render_team_mgmt_combined(mysql)


@login_manager.user_loader
def load_user(id):
    return load_User_O(mysql, int(id))

  
@app.route('/sendJoinRequest/', methods=['GET', 'POST'])
@login_required
def choose_how_to_send_join_request():
    return render_choose_how_to_send_join_request()

  
@app.route('/sendJoinRequestByTid/', methods=['GET', 'POST'])
@login_required
def send_join_request_by_tid():
    return render_send_join_team_message(mysql, by_tid=True)

  
@app.route('/sendJoinRequestByCompanyName/', methods=['GET', 'POST'])
@login_required
def send_join_request_by_company_name():
    return render_send_join_team_message(mysql,by_tid=False)


@app.route('/jobPostingsMgmt/', methods=['GET', 'POST'])
@login_required
def manage_job_postings():
    return render_job_posting_management(mysql)

@app.route('/jobPostings/<tid>/', methods=['GET','POST'])
@login_required
def display_job_postings(tid):
    return render_job_postings_by_company(mysql, tid)

@app.route('/postJob/', methods=['GET', 'POST'])
@login_required
def post_new_job():
    return render_post_new_job(mysql)

@app.route('/applyToJob/<jid>/', methods=['GET', 'POST'])
@login_required
def apply_to_job(jid):
    return render_job_application(mysql, jid)


if __name__ == "__main__":
    app.run(debug=True)
