from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from populatedatabase import populate3

# EP-2: Display Team
def getTeam(tid, mysql):
    cur = mysql.connection.cursor()
    q = "With temp as (Select Users.uid, Users.name, Users.contact, Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.type, temp.contact from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    # q = "With temp as (Select Users.uid, Users.name,Roles.type from Users inner join Roles on Users.rid=Roles.rid) Select temp.name, temp.type from temp, Teams where Teams.uid=temp.uid and Teams.tid="+str(tid)
    resultValue = cur.execute(q)
    if resultValue > 0:  # there are values in the database
        userDetails = cur.fetchall()
        print(type(userDetails))    # tuple
        print(userDetails)          # (('Tim', 'admin'), ('Paula', 'admin'), ('Pritish', 'CEO'))
        return render_template('displayteam.html', userDetails=userDetails)
    else:
        message = "Your team does not exist"
        return render_template('displayteam.html', message=message)
