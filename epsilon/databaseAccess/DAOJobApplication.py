from datetime import datetime
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
        # column order: jap_id, jid, uid, sid, skills, create_date
        for d in data:
            applications.append(JobApplication(jap_id=d[0], jid=d[1], uid=d[2],
                                               sid=d[3], skills=d[4].split(","),
                                               create_date=d[5]))
        return applications

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

    def add_dummy_job_applications(self) -> None:
        """
        Populate JobApplication table with dummy data.
        :requires: Job Postings of jid 1, 2 and 3 to be created.
        """
        job1 = JobApplication(jap_id=1, jid=1, uid=3, sid=RStatus.APPLIED.value,
                              skills="HTML,CSS,JavaScript,JQuery,Bootstrap,React, "
                              + "work in Amazon as a web developer for a year")
        job2 = JobApplication(jap_id=2, jid=1, uid=4, sid=RStatus.INTERVIEW.value,
                              skills="web develop,HTML,MySQL,Bootstrap,"
                              + "React,MongoDB.")
        job3 = JobApplication(jap_id=3, jid=2, uid=3, sid=RStatus.APPLIED.value,
                              skills="manage multiple social media accounts,"
                              + "social media master in SSO.")
        job4 = JobApplication(jap_id=3, jid=3, uid=5, sid=RStatus.OFFER.value,
                              skills="Just please hire me, I will show you my awesome "
                              + "resume if you contact me.")

        jobs_to_add = [job1, job2, job3, job4]

        for job in jobs_to_add:
            self.add_job_application(job)

    def get_job_postings(self) -> List[JobApplication]:
        """
        Gets all job applications in the database.
        :return: List of JobApplication objects.
        """
        job_applications = []
        data = self.get_data('''SELECT * FROM JobApplication''', None)
        for job in data:
            job_applications.append(JobApplication(job[0],job[1],job[2],job[3],
                                                   str(job[4].split(",")),job[5]))
        return job_applications
