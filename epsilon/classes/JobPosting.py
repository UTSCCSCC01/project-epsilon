from flask_login import UserMixin
from datetime import datetime

class JobPosting(UserMixin):
    def __init__(self, jid=0, tid=0, title="default posting",
                 description="default description",
                 create_date=datetime.now().strftime("%m/%d/%Y"), active=True):
        """
        :param jid: job posting id. unique identifier.
        :param tid: team that posted this job.
        :param title: job title.
        :param description: job description.
        :param create_date: default to today.
        :param active: whether startup users can apply to it. Default to yes.
        """
        self._jid = jid
        self._tid = tid
        self._title = title
        self._description = description
        self._create_date = create_date
        self._active = active

    @property
    def jid(self):
        return self._jid

    @jid.setter
    def jid(self, jid):
        self._jid = jid

    @property
    def tid(self):
        return self._tid

    @tid.setter
    def tid(self, tid):
        self._tid = tid

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def create_date(self):
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        self._create_date = create_date

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, active):
        self._active = active

    def __str__(self):
        """ Overloads str method. """
        return 'JobPosting(jid = ' + str(self.jid) \
            + ', tid = ' + str(self.tid) \
            + ', title = ' + self.title \
            + ', description = ' + self.description \
            + ', create_date = ' + str(self.create_date)\
            + ', active = ' + str(self.active) + ')'
