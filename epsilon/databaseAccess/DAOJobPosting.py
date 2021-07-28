from datetime import datetime
from typing import List
from .DAO import DAO
from classes.RStatus import RStatus
from classes.JobPosting import JobPosting


class DAOJobPosting(DAO):
    """
    contains database access methods related to Job Postings.
    """

    def __init__(self, db):
        super().__init__(db)

    def create_job_posting_table(self) -> None:
        """
        Creates the job posting table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS JobPosting ("
                        "jid INTEGER auto_increment,"
                        "tid INTEGER, "
                        "title text, "
                        "description text, "
                        "create_date DATETIME default current_timestamp null,"
                        "active BOOLEAN,"
                        "PRIMARY KEY(jid)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Company table to be created.
        """
        super().add_foreign_key(t_name="JobPosting", f_key="tid", ref_t_name="Company")

    def add_job_posting(self, posting: JobPosting) -> None:
        """
        Adds a new job posting into the database.
        :param posting: The JobApplication object.
        """
        self.modify_data(
            '''INSERT INTO JobPosting (tid, title, description, active)
            VALUES (%s, %s, %s, %s, %s)''',
            (posting.tid,
             posting.title,
             posting.description,
             posting.active))

    def add_dummy_job_postings(self) -> None:
        """
        Populate JobPosting table with dummy data.
        :requires: Companies of tid 1 and 2 to be created.
        """
        job1 = JobPosting(jid=1, tid=1, title="Web developer",
                          description="We want to create our own website! If you are young in heart like us "
                          + "and have at least 5 years of web development experience, please join us!")
        job2 = JobPosting(jid=2, tid=1, title="Marketer",
                          description="We want someone experienced to assist in bringing our startup to the public light! "
                          + "If you are proficient in CRM and knows the perks to be heard, apply to Epsilon!")
        job3 = JobPosting(jid=3, tid=2, title="Financial Officer",
                          description="In this position, you will be doing: work closely with the team to "
                          + "ensure everyone's success, manage the company's financial assests")

        jobs_to_add = [job1, job2, job3]

        for job in jobs_to_add:
            self.add_job_posting(job)

    def get_job_postings(self) -> List[JobPosting]:
        """
        Gets all job postings in the database.
        :return: List of JobPosting objects.
        """
        job_postings = []
        data = self.get_data('''SELECT * FROM JobPosting''', None)
        for job in data:
            job_postings.append(JobPosting(job[0],job[1],job[2],job[3],job[4],job[5]))
        return job_postings
