from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from populatedatabase import add_data


def team_request_load(mysql, tid):
    # Create a table with 5 users. 2 admin and 3 normal users
    #try:
    cur = mysql.connection.cursor()
    sql_q = '''SELECT uid, creation_date FROM Request WHERE tid = %s AND sid = 3 ORDER BY creation_date'''
    cur.execute(sql_q,(tid,))
    data = cur.fetchall()
    #except Exception as e:
    #    return e
    return data