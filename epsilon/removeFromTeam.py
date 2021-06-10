from flask import Flask
from flask_mysqldb import MySQL

# ask kobe if this should be its own thing or if it should piggy back off his add data
# def updateData(mysql, sql_q, data):

def removeFromTeam(mysql):
    cur = mysql.connection.cursor()
    # replace 1s with references to real user data
    cur.execute('''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''',(1,1))
    mysql.connection.commit()