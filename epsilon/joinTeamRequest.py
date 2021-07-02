from classes.Role import Role
from classes.Team import Team
from classes.RStatus import RStatus
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from DAO import DAO

def team_request_accept(dao, req_id):
    # Update Request and Teams to reflect on accept action
    message = team_request_update(dao, req_id, RStatus.ACCEPTED.value)

    if message is None:
        request = dao.get_request(req_id)
        team = Team(request.tid, request.uid, Role.TEAM_MEMBER.value)
        dao.add_team(team)
        dao.update_role_of_employee(request.uid, Role.TEAM_MEMBER.value)
        message = "Accept Successful!"
    return message


def team_request_decline(dao, req_id):
    # Update Request to reflect on decline action
    message = team_request_update(dao, req_id, RStatus.REJECTED.value)
    if message is None:
        message = "Decline Successful!"
    return message


def team_request_update(dao, req_id, status):
    request = dao.get_request(req_id)
    if request.sid == RStatus.PENDING.value:
        dao.update_request_status(req_id, status)
        return
    else:
        return "Status is not pending!"
