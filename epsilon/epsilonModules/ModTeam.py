from classes.JobApplication import JobApplication
from classes.ApplicantDetail import ApplicantDetail
from typing import List
from flask_mysqldb import MySQL
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from exceptions.ObjectExistsError import ObjectExistsError
from exceptions.AccessDeniedError import AccessDeniedError
from exceptions.FormIncompleteError import FormIncompleteError
from classes.Team import Team
from classes.Role import Role
from classes.Request import Request
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOUser import DAOUser
from databaseAccess.DAORStatus import DAORStatus
from databaseAccess.DAOJobApplication import DAOJobApplication
from flask_login import current_user
from classes.Type import Type
from classes.RStatus import RStatus


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


def check_join_requests_by_tid_uid_status(mysql: MySQL, tid: int, uid:int, status_choice:List[int])->bool:
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


def get_user_teams(mysql: MySQL, uid: int) -> List[Team]:
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

def get_applicant_details(mysql: MySQL, tid: int) -> List[ApplicantDetail]:
    """
    Get a list of application details of applicants of a company of tid.
    :param mysql: mysql db.
    :param tid: the tid of company.
    :return: list of ApplicationDetails Objects.
    """
    dao_company = DAOCompany(mysql)
    dao_job_application = DAOJobApplication(mysql)
    dao_rstatus = DAORStatus(mysql)
    company = dao_company.get_company_by_tid(tid)
    if not company:
        raise ObjectNotExistsError("Your company")
    applicants = dao_job_application.get_applicant_details_by_tid(tid)
    for applicant in applicants:
        rstatus = dao_rstatus.get_status_by_sid(applicant.sid)
        rstatus_name = rstatus.name.title()
        applicant.jap_status = rstatus_name
    return applicants


def update_jap_to_rstatus(mysql: MySQL, jap_id: int, status: RStatus):
    """
    Updates job application of id jap_id to status.
    :param mysql: The MySQL db.
    :param req_id: request id of request.
    :param status: sid to update to.
    :return successful message.
    """
    dao_job_application = DAOJobApplication(mysql)
    job_app = dao_job_application.get_job_application_by_jap_id(jap_id)
    if (job_app.sid == RStatus.APPLIED.value and status == RStatus.INTERVIEW) or\
       (job_app.sid == RStatus.INTERVIEW.value and status == RStatus.OFFER) or\
       (job_app.sid == RStatus.OFFER.value and status == RStatus.ACCEPTED) or\
       (job_app.sid == RStatus.OFFER.value and status == RStatus.DECLINED) or\
       status == RStatus.REJECTED:
        job_app.sid = status.value
        dao_job_application.update_job_application_status(job_app)
        return "Updated the status of the job application to " + status.name.title() + "!"
    else:
        return "An error occured when updating the status of the job application!"