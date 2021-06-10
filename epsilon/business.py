from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from populatedatabase import add_data


def team_request_load(mysql, tid):
    # Get data for pending join team requests
    cur = mysql.connection.cursor()
    sql_q = '''SELECT uid, creation_date, req_id FROM Request WHERE tid = %s AND sid = 3 ORDER BY creation_date'''
    cur.execute(sql_q,(tid,))
    data = cur.fetchall()
    return data

def team_request_accept(mysql, req_id):
    # Update Request and Teams to reflect on accept action
    team_request_update(mysql, req_id, 1)

    cur = mysql.connection.cursor()
    sql_q = '''SELECT tid, uid FROM Request WHERE req_id = %s'''
    cur.execute(sql_q,(req_id,))
    data = cur.fetchone()
    sql_q = '''INSERT INTO Teams VALUES (%s, %s, 3)'''
    data = (data[0], data[1])
    add_data(mysql, sql_q, data)
    return

def team_request_decline(mysql, req_id):
    # Update Request to reflect on decline action
    team_request_update(mysql, req_id, 2)

    return

def team_request_update(mysql, req_id, status):
    sql_q = '''UPDATE Request Set sid = %s, last_update = %s, seen = false WHERE req_id = %s'''
    data = (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), req_id)
    add_data(mysql, sql_q, data)
    return