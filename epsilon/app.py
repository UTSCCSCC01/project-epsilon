from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from populatedatabase import populate, add_data
from populatedatabase import populate3

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
@app.route("/deleteAll")
def delete_all():
    cur1 = mysql.connection.cursor()
    cur1.execute('''DROP TABLE IF EXISTS Users''')
    cur1.execute('''DROP TABLE IF EXISTS Teams''')
    cur1.execute('''DROP TABLE IF EXISTS Roles''')
    mysql.connection.commit()
    return "Database Users, Teams are deleted!"

@app.route("/create")
def create():
    populate(mysql)
    populate3(mysql)
    cur1 = mysql.connection.cursor()
    cur1.execute('''SELECT * FROM Users''')
    cur2 = mysql.connection.cursor()
    cur2.execute('''SELECT * FROM Teams''')
    cur3 = mysql.connection.cursor()
    cur3.execute('''SELECT * FROM Roles''')
    return "Database Users, Teams, Roles are populated!\n" \
           "Also five dummy employees Paula, Tim, Pritish, Sam, Water."+"\n\n"\
           +str(cur1.fetchall())+"\n\n"+str(cur2.fetchall())\
           +"\n\n"+str(cur3.fetchall())

# EP-1: Team management


def is_pos_int(s):
    try:
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    # TODO: check if user is logged in and check permissions
    # cur = mysql.connection.cursor()
    if request.method == 'POST':
        # create both queries for checking and inserting data
        sql_q = '''INSERT INTO Teams VALUES (%s, %s, 1)'''
        # check if all form boxes are completed
        if (len(request.form['teamid']) == 0 or len(request.form['userid']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('registration.html', error=error)
        # check if all form boxes are integers
        if not (is_pos_int(request.form['teamid']) and is_pos_int(request.form['userid'])):
            error = 'team id and user id are in digit format'
            return render_template('registration.html', error=error)
        # check if input int is out of range of mySql, just for demo purpose
        if int(request.form['teamid']) > 2147483647 or int(request.form['userid']) > 2147483647:
            error = 'Id number is too large'
            return render_template('registration.html', error=error)
        # if no errors
        try:
            message = add_data(
                mysql, sql_q, (request.form['teamid'], request.form['userid']))
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message)
    else:
        # load if not POST
        return render_template("registration.html")

# result is returned correctly, just need todispaly


@app.route("/displayteam/<int:tid>/", methods=['GET'])
def display_team(tid):
    cur = mysql.connection.cursor()
    # q = "With temp as (Select Users.uid, Users.name,Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.contact, temp.type from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    q = "With temp as (Select Users.uid, Users.name,Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.type from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    resultValue = cur.execute(q)
    if resultValue > 0:  # there are values in the database
        userDetails = cur.fetchall()
        print(userDetails)
        return render_template('displayteam.html', userDetails=userDetails)
    else:
        message = "Your team does not exist"
        return render_template('displayteam.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
