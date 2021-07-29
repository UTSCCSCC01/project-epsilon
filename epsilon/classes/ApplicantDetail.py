from datetime import datetime
from classes.JobApplication import JobApplication


class ApplicantDetail(JobApplication):
    def __init__(self, jap_id=0, jid=0, uid=0, sid=0,
                skills=[], create_date=datetime.now(),
                user_name="", user_contact="", job_title="", jap_status="", user_description=""):
        """
        Child class of JobApplication
        :param jap_id: job application id, unique identifier.
        :param jid: job posting id that this application applied for.
        :param uid: candidate id.
        :param sid: status id, default to APPLIED.
        :param create_date: default to today.
        :param skills: list of skills.
        :param user_name: the name of the user of uid.
        :param user_contact: the contact of the user of uid.
        :param job_title: the job title of the posting of jid.
        :param user_description: the description of the user of uid.
        """        
        super().__init__(jap_id,jid, uid, sid, skills, create_date)
        self._user_name = user_name
        self._user_contact = user_contact
        self._job_title = job_title
        self._jap_status = jap_status
        self._user_description = user_description

    @property
    def user_name(self):
        return self._user_name
    
    @user_name.setter
    def user_name(self, user_name):
        self._user_name = user_name

    @property
    def user_contact(self):
        return self._user_contact

    @user_contact.setter
    def user_contact(self, user_contact):
        self._user_contact = user_contact
    
    @property
    def job_title(self):
        return self._job_title
    
    @job_title.setter
    def job_title(self, job_title):
        self._job_title = job_title

    @property
    def jap_status(self):
        return self._jap_status
    
    @jap_status.setter
    def jap_status(self, jap_status):
        self._jap_status = jap_status

    @property
    def user_description(self):
        return self._user_description
    
    @user_description.setter
    def user_description(self, user_description):
        self._user_descriptions = user_description
    
    def __str__(self):
        """ Overloads str method. """
        return 'ApplicantDetails(jap_id = ' + str(self.jap_id) \
            + ', jid = ' + str(self.jid) \
            + ', uid = ' + str(self.uid) \
            + ', sid = ' + str(self.sid) \
            + ', create_date = ' + str(self.create_date) \
            + ', skills = ' + self.skills \
            + ', user_name = ' + self.user_name \
            + ', user_contact = ' + self.user_contact \
            + ', job_title = ' + self.job_title \
            + ', jap_status = ' + self.jap_status \
            + ', user_description = ' + self.user_description + ')'
