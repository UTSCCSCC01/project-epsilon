from typing import List
from .DAO import DAO
from classes.RStatus import RStatus
from classes.JobApplication import JobApplication


class DAOJobApplication(DAO):
    """
    contains database access methods related to Job Application.
    """

    def __init__(self, db):
        super().__init__(db)

    def create_job_application_table(self) -> None:
        """
        Creates the job application table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS JobApplication ("
                        "jap_id INTEGER auto_increment,"
                        "jid INTEGER, "
                        "uid INTEGER, "
                        "sid INTEGER, "
                        "skills text, "
                        "create_date DATETIME default current_timestamp null,"
                        "PRIMARY KEY(jap_id)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: JobPosting, Users and RStatus tables to be created.
        """
        super().add_foreign_key(t_name="JobApplication", f_key="jid", ref_t_name="JobPosting")
        super().add_foreign_key(t_name="JobApplication", f_key="uid", ref_t_name="Users")
        super().add_foreign_key(t_name="JobApplication", f_key="sid", ref_t_name="RStatus")

    def add_job_application(self, application: JobApplication) -> None:
        """
        Adds a new job application into the database.
        :param application: The JobApplication object.
        """
        self.modify_data(
            '''INSERT INTO JobApplication (jid, uid, sid, skills)
            VALUES (%s, %s, %s, %s)''',
            (application.jid,
             application.uid,
             application.sid,
             application.skills))


    def update_job_application_status(self, application: JobApplication) -> None:
        """
        Updates the status an existing job application.
        :param application: New JobApplication object.
        jap_id and sid cannot be None.
        """
        self.modify_data(
            '''UPDATE JobApplication Set sid = %s, seen = false WHERE jap_id = %s''',
            (application.sid, application.jap_id))

    def get_job_application_by_uid(self, uid: int) -> List[JobApplication]:
        """
        Gets all job applications for user with <uid>, latest comes
        first.
        :param uid: uid id of the user to be retrieved.
        :return: all JobApplication representing the matching request.
                 None if no application of user does not exist.
        """
        applications = []
        data = self.get_data('''SELECT * FROM JobApplication
                                WHERE uid = %s
                                ORDER BY create_date DESC''',
                             (uid,))
        for d in data:
            applications.append(JobApplication(jap_id=d[0], jid=d[1], uid=d[2],
                                               sid=d[3], skills=d[4].split(","),
                                               create_date=d[5]))
        return applications


    def check_job_application_exists_by_uid_jid(self, uid: int, jid:int) -> bool:
        """
        Check whether uid applied to the job jid before.
        :param uid: uid id of the user to be retrieved.
        :param jid: jid of job to check.
        :return: whether such application exist.
        """
        data = self.get_data('''SELECT * FROM JobApplication
                                WHERE uid = %s AND jid=%s
                                ORDER BY create_date DESC''',
                             (uid,jid,))
        return len(data) > 0

    def get_job_application_by_jap_id(self, jap_id: int) -> JobApplication:
        """
        Gets a unique job application from the database.
        :param jap_id: application id.
        :return: JobApplication object.
                 None if not found.
        """
        res = None
        d = self.get_data('''SELECT *
                             FROM JobApplication WHERE jap_id = %s''', (jap_id,))
        if d is not None:
            res=JobApplication(jap_id=d[0], jid=d[1], uid=d[2],
                                sid=d[3], skills=str(d[4]).split(","),
                                create_date=d[5])
        return res

    def send_job_application(self, jid: int, uid: int, skills: str):
        """
        Sends a job application.
        :param jid: job id.
        :param uid: user id.
        :param skills: the skills  the user used to apply to this job.
        """
        application = JobApplication(jid=jid, uid=uid,
                                     sid=RStatus.APPLIED.value, skills=skills)
        self.add_job_application(application=application)