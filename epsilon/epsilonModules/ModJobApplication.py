from databaseAccess.DAOJobApplication import DAOJobApplication
from databaseAccess.DAORStatus import DAORStatus
from classes.JobApplication import JobApplication
from classes.ApplicantDetail import ApplicantDetail
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from typing import List
from flask_mysqldb import MySQL


def get_applicant_profile(mysql: MySQL, jap_id: int) -> ApplicantDetail:
    """
    Get application detail of the application of jap_id.
    :param mysql: mysql db.
    :param jap_id: the jap_id of application.
    :return: an ApplicationDetail Object.
    """
    dao_job_application = DAOJobApplication(mysql)
    dao_rstatus = DAORStatus(mysql)
    applicant = dao_job_application.get_applicant_details_by_jap_id(jap_id)
    if applicant is None:
        raise ObjectNotExistsError("The Job Application")
    rstatus = dao_rstatus.get_status_by_sid(applicant.sid)
    rstatus_name = rstatus.name.title()
    applicant.jap_status = rstatus_name
    return applicant