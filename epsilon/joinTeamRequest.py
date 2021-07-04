from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAOTeam import DAOTeam
from classes.Role import Role
from classes.Team import Team
from classes.RStatus import RStatus
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime
from databaseAccess.DAO import DAO


def team_request_accept(mysql, req_id):
    # Update Request and Teams to reflect on accept action
    dao_request = DAORequest(mysql)
    dao_team = DAOTeam(mysql)
    message = team_request_update(dao_request, req_id, RStatus.ACCEPTED.value)

    if message is None:
        request = dao_request.get_request_by_req_id(req_id)
        team = Team(request.tid, request.uid, Role.TEAM_MEMBER.value)
        dao_team.add_team(team)
        message = "Accept Successful!"
    return message


def team_request_decline(mysql, req_id):
    # Update Request to reflect on decline action
    dao_request = DAORequest(mysql)
    message = team_request_update(dao_request, req_id, RStatus.REJECTED.value)
    if message is None:
        message = "Decline Successful!"
    return message


def team_request_update(dao_request, req_id, status):
    request = dao_request.get_request_by_req_id(req_id)
    if request.sid == RStatus.PENDING.value:
        request.sid = status
        dao_request.update_request(request)
        return
    else:
        return "Status is not pending!"
