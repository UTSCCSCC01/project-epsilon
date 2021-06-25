class Team:
    def __init__(self, tid=0, uid=0, rid=0):
        self._tid = tid
        self._uid = uid
        self._rid = rid

    @property
    def tid(self):
        return self._tid

    @tid.setter
    def tid(self, tid):
        self._tid = tid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def rid(self):
        return self._rid

    @rid.setter
    def rid(self, rid):
        self._rid = rid

    def __str__(self):
        """ Overloads str method. """
        return 'Team(tid = ' + str(self.tid) + ', uid = ' + str(self.uid) + ', rid = ' + str(self.rid) + ')'
