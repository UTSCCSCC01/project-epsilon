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
            '''INSERT INTO JobPosting (jid, tid, title, description, active)
            VALUES (%s, %s, %s, %s, %s)''',
            (posting.jid,
             posting.tid,
             posting.title,
             posting.description,
             posting.active))
