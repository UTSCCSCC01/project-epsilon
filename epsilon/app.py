from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from populatedatabase import populate, add_data, populate2

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
    return "Database Users, Teams are populated!"

# EP-1: Team management

def is_pos_int(s):
    try:
        if int(s)>0:
            return True
        else:
            return False
    except ValueError:
        return False

@app.route('/manageteam', methods=['GET', 'POST'])
def manageteam():
    # TODO: check if user is logged in and check permissions
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        # create both queries for checking and inserting data
        sql_q = '''INSERT INTO Teams VALUES (%s, %s, 1)'''
        # check if all form boxes are completed
        if (len(request.form['teamid']) == 0 or len(request.form['userid']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('manageteam.html', error=error)
        # check if all form boxes are integers
        if not (is_pos_int(request.form['teamid']) and  is_pos_int(request.form['userid'])):
            error = 'team id and user id are in digit format'
            return render_template('manageteam.html', error=error)
        # check if input int is out of range of mySql, just for demo purpose
        if int(request.form['teamid'])>2147483647 or int(request.form['userid'])>2147483647:
            error = 'Id number is too large'
            return render_template('manageteam.html', error=error)
        # if no errors
        try:
            message = add_data(
                mysql, sql_q, (request.form['teamid'], request.form['userid']))
        except Exception as e:
            return render_template('manageteam.html', error=e)
        return render_template('manageteam.html', message=message)
    else:
        # load if not POST
        return render_template("manageteam.html")

# Only go to this page after you go to /create to add more tables and add key constraints 

# EP-3: Accept and Decline pending requests
@app.route("/create2")
def create2():
    populate2(mysql)
    return "Database Roles, Company, Request and Status are populated!"

if __name__ == "__main__":
    app.run(debug=True)
