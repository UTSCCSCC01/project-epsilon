from flask_login import UserMixin
from datetime import datetime

class JobApplication(UserMixin):
    def __init__(self, jap_id=0, jid=0, uid=0, sid=1,
                 skills=None, create_date=datetime.now().strftime("%m/%d/%Y")):
        """
        :param jap_id: job application id, unique identifier.
        :param jid: job posting id that this application applied for.
        :param uid: candidate id.
        :param sid: status id, default to APPLIED.
        :param create_date: default to today.
        :param skills: list of skills.
        """
        self._jap_id = jap_id
        self._jid = jid
        self._uid = uid
        self._sid = sid
        self._create_date = create_date
        if not skills:
            self._skills = []
        else:
            self._skills = skills

    @property
    def jap_id(self):
        return self._jap_id

    @jap_id.setter
    def jap_id(self, jap_id):
        self._jap_id = jap_id

    @property
    def jid(self):
        return self._jid

    @jid.setter
    def jid(self, jid):
        self._jid = jid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def create_date(self):
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        self._create_date = create_date

    @property
    def skills(self):
        return str(self._skills)[1:-1]

    @skills.setter
    def skills(self, skills):
        self._skills = skills

    def __str__(self):
        """ Overloads str method. """
        return 'JobApplication(jap_id = ' + str(self.uid) \
            + ', jid = ' + str(self.jid) \
            + ', uid = ' + str(self.uid) \
            + ', sid = ' + str(self.sid) \
            + ', create_date = ' + self.create_date\
            + ', skills = ' + self.skills + ')'
