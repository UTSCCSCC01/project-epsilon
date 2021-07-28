from typing import List
from flask_mysqldb import MySQL
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from exceptions.ObjectExistsError import ObjectExistsError
from exceptions.AccessDeniedError import AccessDeniedError
from exceptions.FormIncompleteError import FormIncompleteError
from classes.Team import Team
from classes.Role import Role
from classes.RStatus import RStatus
from classes.Request import Request
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOUser import DAOUser
from flask_login import current_user
from classes.Type import Type
from classes.RStatus import RStatus
import traceback


def remove_from_team(mysql: MySQL, tid: int,
                     uid: int, rid: int) -> str:
    """
    Remove member from team. Return successful message
    :param mysql: mysql db.
    :param tid: tid of company.
    :param uid: uid of user.
    :param rid: role of user in company.
    :return: successful message
    """
    dao_team = DAOTeam(mysql)
    if(int(rid) != Role.TEAM_OWNER.value):
        dao_team.remove_from_team(tid, uid)
        return "Remove from team successful!"


def promote_admin(mysql: MySQL, tid: int, uid: int, rid: int) -> str:
    """
    Promote user in company to admin.
    :param mysql: mysql db.
    :param tid: tid of company.
    :param uid: uid of user.
    :param rid: role of user in company.
    :return: successful message
    """
    # newRole should be id of admin
    dao_team = DAOTeam(mysql)
    team_to_update = dao_team.get_team_by_tid_uid(tid, uid)
    if(int(rid) != Role.TEAM_OWNER.value):
        team_to_update.rid = Role.TEAM_ADMIN.value
        dao_team.update_team(team_to_update)
        return "Promote admin successful!"


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
        data.append([user.name, user.contact, req.create_date, req.req_id, user.uid])
    return data, company.name


def check_join_requests_by_tid_uid_status(mysql: MySQL, tid: int, uid:int, status_choice:[int])->bool:
    """
    Check whether there's at least one request with specified tid, uid and
    status given by status_choice. the tid or uid may not exist.
    :param mysql: mysql db.
    :param tid: tid of company.
    :param uid: user id.
    :param status_choice: list of desired status of the requests, can only
    be chosen from: 1(ACCEPTED), 2(REJECTED), 3(PENDING).
    :return: whether data exist.
    """
    dao_request = DAORequest(mysql)
    dao_company = DAOCompany(mysql)
    dao_user = DAOUser(mysql)
    if not dao_company.get_company_by_tid(tid):
        raise ObjectNotExistsError("Your team")
    if not dao_user.get_user_by_uid(uid):
        raise ObjectNotExistsError("The user")
    requests = []
    for status in status_choice:
        new_requests = dao_request.get_requests_by_tid_uid_sid(tid,uid, status)
        if new_requests==None:
            new_requests=[]
        requests.extend(new_requests)
        if len(requests)>0:
            return True
    return False

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

def get_user_teams(mysql: MySQL, uid: int) -> [Team]:
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

def add_join_team_request_by_tid(mysql: MySQL, tid:str, uid:int, type_id:int) -> str:
    """
    Add a join team request to the database, return a message on success
    or raise an error if access is denied or company doesn't exist.
    :param mysql: mysql db.
    :param tid: the id of team to join.
    :param uid: uid of the user.
    :param type_id: the type of user.
    """
    if len(tid)==0:
        raise FormIncompleteError()
    tid=int(tid)
    exist_flag= check_join_requests_by_tid_uid_status(
                                            mysql=mysql, tid=tid,
                                            uid=uid,
                                            status_choice=[
                                                RStatus.PENDING.value,
                                                RStatus.ACCEPTED.value])
    # only create request if this user hasn't created the join request to the
    # company before or it's been declined
    if exist_flag:
        raise ObjectExistsError(obj="a same request from you (accepted or pending)")
    if type_id == Type.STARTUP_USER.value:
        message = "the request was sent successfully."
        dao_req = DAORequest(mysql)
        req = Request(tid=tid, uid=uid, sid=RStatus.PENDING.value)
        dao_req.add_request(req)
        return message
    else:
        raise AccessDeniedError(functionality="send request to join a company.")


def add_join_team_request_by_company_name(mysql: MySQL, company_name:str, uid:int, type_id:int) -> str:
    """
    Add a join team request to the database, return a message on success
    or raise an error if access is denied or company doesn't exist.
    :param mysql: mysql db.
    :param company_name: the name of company to join.
    :param uid: uid of the user.
    :param type_id: the type of user.
    """
    if len(company_name)==0:
        raise FormIncompleteError()
    dao_company= DAOCompany(mysql)
    company = dao_company.get_company_by_name(company_name)
    if company:
        return add_join_team_request_by_tid(mysql=mysql, tid=str(company.tid), uid=uid, type_id=type_id)
    else:
        raise ObjectNotExistsError(obj="the company")

def add_to_team(mysql:MySQL, uid:int, tid:int) -> str:
    """
    For use by join by code to add cur user to team
    :param mysql: db used
    :param uid: uid of user to add
    :param tid: tid for user to join
    :return: response message
    """
    dao_team = DAOTeam(mysql)
    team = Team(tid, uid, Role.TEAM_MEMBER.value)
    try:
        dao_team.add_team(team)
        return "Joined Successfully"
    except Exception as e:
        return e