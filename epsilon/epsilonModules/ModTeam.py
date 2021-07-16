from typing import List
from flask_mysqldb import MySQL
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from classes.Team import Team
from classes.Role import Role
from classes.RStatus import RStatus
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOUser import DAOUser


def remove_from_team(mysql: MySQL, tid: int,
                     uid: int, rid: int) -> None:
    """
    Remove member from team.
    :param mysql: mysql db.
    :param tid: tid of company.
    :param uid: uid of user.
    :param rid: role of user in company.
    """
    dao_team = DAOTeam(mysql)
    if(int(rid) != Role.TEAM_OWNER.value):
        dao_team.remove_from_team(tid, uid)


def promote_admin(mysql: MySQL, tid: int, uid: int, rid: int):
    """
    Promote user in company to admin.
    :param mysql: mysql db.
    :param tid: tid of company.
    :param uid: uid of user.
    :param rid: role of user in company.
    """
    # newRole should be id of admin
    dao_team = DAOTeam(mysql)
    team_to_update = dao_team.get_team_by_tid_uid(tid, uid)
    if(int(rid) != Role.TEAM_OWNER.value):
        team_to_update.rid = Role.TEAM_ADMIN.value
        dao_team.update_team(team_to_update)


def get_members(mysql: MySQL, tid: int) -> List:
    """
    Return the users that has are in the team.
    :param mysql: mysql db.
    :param tid: tid of company.
    :return List of user details of a team.
    """
    dao_team = DAOTeam(mysql)
    dao_role = DAORole(mysql)
    users = dao_team.get_users_from_team(tid)
    if not users:
        raise ObjectNotExistsError("Your team")
    # there are values in the database
    user_details = []
    for user in users:
        role = dao_role.get_role_by_rid(user.rid)
        role_name = role.name.replace("_", " ").title()
        user_details.append([user.name, role_name, user.contact,
                            user.uid, tid, user.rid])
    return user_details


def get_join_requests(mysql: MySQL, tid: int):
    """
    Return a list of request details and the company name.
    :param mysql: mysql db.
    :param tid: tid of company.
    :return list of request details and the company name.
    """
    dao_request = DAORequest(mysql)
    dao_company = DAOCompany(mysql)
    dao_user = DAOUser(mysql)

    requests = dao_request.get_requests_by_tid_sid(tid, RStatus.PENDING.value)
    company = dao_company.get_company_by_tid(tid)
    if not company:
        raise ObjectNotExistsError("Your team")
    data = []
    for req in requests:
        user = dao_user.get_user_by_uid(req.uid)
        data.append([user.name, req.create_date, req.req_id])
    return data, company.name


def team_request_accept(mysql: MySQL, req_id: int) -> str:
    """
    Updates request of id req_id to accpet and add the user to team as member.
    :param mysql: mysql db.
    :param req_id: request id of request.
    :return status message of accept.
    """
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


def team_request_decline(mysql: MySQL, req_id: int) -> str:
    """
    Updates request of id req_id to decline.
    :param mysql: mysql db.
    :param req_id: request id of request.
    :return status message of decline.
    """
    # Update Request to reflect on decline action
    dao_request = DAORequest(mysql)
    message = team_request_update(dao_request, req_id, RStatus.REJECTED.value)
    if message is None:
        message = "Decline Successful!"
    return message


def team_request_update(dao_request: DAORequest, req_id: int, status: int):
    """
    Updates request of id req_id to status.
    :param dao_company: The DAO object for Request class
    :param req_id: request id of request.
    :param status: sid to update to.
    :return None if successful, error message if sid is not pending.
    """
    request = dao_request.get_request_by_req_id(req_id)
    if request.sid == RStatus.PENDING.value:
        request.sid = status
        dao_request.update_request(request)
        return None
    else:
        return "Status is not pending!"


def get_user_teams(mysql: MySQL, uid: int) -> List:
    """
    Returns the data of the teams that user with uid is in
    :param mysql: mysql db.
    :param uid: uid of the user.
    :Return a list of team details.
    """
    dao_team = DAOTeam(mysql)
    teams = dao_team.get_teams_by_uid(uid)
    if not teams:
        raise ObjectNotExistsError("The Team")
    return teams


def add_team(mysql: MySQL, tid: int, uid: int):
    """
    Add's a team to the database
    :param mysql: mysql db.
    :param uid: uid of the user.
    """
    dao_team = DAOTeam(mysql)
    team = Team(tid, uid, Role.TEAM_OWNER.value)
    dao_team.add_team(team)
