from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from populatedatabase import populate, add_data
from registration import registration

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'epsilon'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'epsilon_db'

mysql = MySQL(app)


@app.route("/")
def hello():
    return "Hello World! Welcome to Epsilon!"

# Only go to this page if your database is empty


@app.route("/create")
def create():
    populate(mysql)
    return "Database Users, Teams, Company are populated!"

# EP-1: Team management
def is_pos_int(s):
    try:
        if int(s)>0:
            return True
        else:
            return False
    except ValueError:
        return False

@app.route('/registration', methods=['GET', 'POST'])
def reg():
    return registration(mysql)


if __name__ == "__main__":
    app.run(debug=True)
