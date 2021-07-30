from typing import List
from .DAO import DAO
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
            VALUES (%s, %s, %s, %s)''',
            (posting.tid,
             posting.title,
             posting.description,
             posting.active))

    def post_new_job(self, tid: int, title: str, description: str):
        posting = JobPosting(tid=tid, title=title, description=description, active=True)
        self.add_job_posting(posting=posting)

    def update_job_posting_status(self, jid: int, new_status: bool) -> None:
        """
        Update the active status of a job posting.
        :param jid: The id of the posting to reverse.
        :param new_status: The new status.
        """
        self.modify_data(
            '''UPDATE JobPosting Set active = %s WHERE jid = %s''',
            (new_status, jid))

    def get_status_of_job_posting(self, jid: int) -> bool:

        data = self.get_data('''SELECT active FROM JobPosting
                                WHERE jid = %s''',
                             (jid,))
        if len(data) == 0:
            return None
        else:
            return bool(data[0][0])

    def get_job_postings_by_tid(self, tid: int, active_only=False) -> List[JobPosting]:
        postings = []
        if active_only:
            query = '''SELECT title, description, create_date, active, jid FROM JobPosting
                                    WHERE tid = %s AND active=1
                                    ORDER BY create_date DESC'''
        else:
            query = '''SELECT title, description, create_date, active, jid FROM JobPosting
                                WHERE tid = %s
                                ORDER BY active DESC, create_date DESC'''

        job_postings = self.get_data(query, (tid,))

        for posting in job_postings:
            postings.append(JobPosting(title=posting[0], description=posting[1],
                                       create_date=posting[2], active=posting[3], jid=posting[4]))
        return postings

    def get_job_posting_by_jid(self, jid: int) -> JobPosting:
        """
        Return a job posting corresponding to the given jid.
        :param jid: Job ID of the job posting.
        :return: JobPosting object corresponding to the jid.
        """
        job_posting = None
        data = self.get_data('''SELECT * FROM JobPosting WHERE jid = %s''', (jid,))

        if data:
            job_posting = data[0]
            job_posting = JobPosting(jid=job_posting[0], tid=job_posting[1], title=job_posting[2],
                                     description=job_posting[3], create_date=job_posting[4], active=job_posting[5])
        return job_posting
