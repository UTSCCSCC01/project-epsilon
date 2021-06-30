from classes.Team import Team
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from DAO import DAO


def team_request_load(dao, tid):
    # Get data for pending join team requests
    sql_q = '''SELECT uid, create_date, req_id FROM Request WHERE tid = %s AND sid = 3 ORDER BY create_date'''
    data = dao.get_data(sql_q, (tid,))
    return data

def team_request_accept(dao, req_id):
    # Update Request and Teams to reflect on accept action
    message = team_request_update(dao, req_id, 1)

    if message == None:
        sql_q = '''SELECT tid, uid FROM Request WHERE req_id = %s'''
        data = dao.get_data(sql_q, (req_id,))
        sql_q = '''INSERT INTO Teams VALUES (%s, %s, 3)'''
        update = (data[0][1])
        dao.update_role_of_employee(update, 3)
        data = (data[0][0], data[0][1])
        dao.modify_data(sql_q, data)
    if message is None:
        request = dao.get_request(req_id)
        team = Team(request.tid, request.uid, 3)
        dao.update_role_of_employee(request.uid, 3)
        dao.add_team(team)
        message = "Accept Successful!"
    return message


def team_request_decline(dao, req_id):
    # Update Request to reflect on decline action
    message = team_request_update(dao, req_id, 2)
    if message == None:
    if message is None:
        message = "Decline Successful!"
    return message


def team_request_update(dao, req_id, status):
    sql_q = '''SELECT sid FROM Request WHERE req_id = %s'''
    data = dao.get_data(sql_q, (req_id,))
    if data[0][0] == 3:
        sql_q = '''UPDATE Request Set sid = %s, last_update = %s, seen = false WHERE req_id = %s'''
        data = (status, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), req_id)
        dao.modify_data(sql_q, data)
    request = dao.get_request(req_id)
    if request.sid == 3:
        dao.update_request_status(req_id, status)
        return
    else:
        return "Status is not pending!"        return "Status is not pending!"
        return "Status is not pending!"
