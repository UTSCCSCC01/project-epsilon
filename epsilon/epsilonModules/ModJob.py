from flask_mysqldb import MySQL
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from exceptions.ObjectExistsError import ObjectExistsError
from exceptions.AccessDeniedError import AccessDeniedError
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOJobPosting import DAOJobPosting
from databaseAccess.DAOJobApplication import DAOJobApplication
from classes.Type import Type
from classes.JobPosting import JobPosting
from classes.Role import Role


def validate_team_admin(role_id: int):
    if role_id != Role.TEAM_ADMIN.value:
        raise AccessDeniedError(role="non team admin member", functionality="manage the job postings of your company")

def validate_startup_user(type_id: int):
    if type_id != Type.STARTUP_USER.value:
        raise AccessDeniedError(functionality="see the job postings")

def reverse_status_of_job_posting(mysql: MySQL, jid: int):
    """
    reverse job jid from active to deactivated, or deactivated to active.
    :param mysql: mysql db.
    :param jid: job posting id.
    """
    dao_jobposting = DAOJobPosting(mysql)
    curr_status = dao_jobposting.get_status_of_job_posting(jid)
    if curr_status is not None:
        dao_jobposting.update_job_posting_status(jid=jid, new_status=not curr_status)
    else:
        raise ObjectNotExistsError(obj="this job posting")

def get_job_postings_by_tid(mysql: MySQL, tid: int, active_only=False) -> [JobPosting]:
    """
    Returns all job postings of a company.
    If active_only, then only return active jobs.
    :param tid: team id.
    :Return a list of JobPostings.
    """
    dao_jobposting = DAOJobPosting(mysql)
    postings = dao_jobposting.get_job_postings_by_tid(tid, active_only)
    return postings


def check_existence_of_application(mysql: MySQL, jid: int, uid: int):
    dao_job_application = DAOJobApplication(mysql)
    if dao_job_application.check_job_application_exists_by_uid_jid(uid=uid, jid=jid):
        raise ObjectExistsError("Your application to this job")

def apply_to_job(mysql: MySQL, jid: int, uid: int, skills: str):
    """
    Apply to a job by given jid and user id, skills.
    :param jid: job posting id.
    :param uid: user id.
    :param skills: skills used to apply.
    """
    check_existence_of_application(mysql,jid, uid)
    dao_job_application = DAOJobApplication(mysql)
    dao_job_application.send_job_application(jid, uid, skills)
    return "application sent."

def post_job(mysql: MySQL, tid: int, title: str, description:str):
    """
    Post a job by given info
    :param tid: team id.
    :param title: job title.
    :param description: job description.
    """
    dao_job_posting = DAOJobPosting(mysql)
    dao_job_posting.post_new_job(tid=tid, title=title, description=description)
    return "Job Posted."

def get_tid_by_admin_uid(mysql: MySQL, uid:int) -> [int]:
    dao_team = DAOTeam(mysql)
    tid_list = dao_team.get_tids_by_admin_uid(uid=uid)
    return tid_list
