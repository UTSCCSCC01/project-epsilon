from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from populatedatabase import populate, add_data

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
    return "Database is populated!"

# EP-1: Team management


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
        # if no errors
        message = add_data(
            mysql, sql_q, (request.form['teamid'], request.form['userid']))
        return render_template('manageteam.html', message=message)
    else:
        # load if not POST
        return render_template("manageteam.html")


if __name__ == "__main__":
    app.run(debug=True)
