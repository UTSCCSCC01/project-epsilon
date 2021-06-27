class Request:
    def __init__(self, req_id=0, tid=0, uid=0, sid=0, create_date="", last_update="", seen=-1):
        self._req_id = req_id
        self._tid = tid
        self._uid = uid
        self._sid = sid
        self._create_date = create_date
        self._last_update = last_update
        self._seen = seen

    @property
    def req_id(self):
        return self._req_id

    @req_id.setter
    def req_id(self, req_id):
        self._req_id = req_id

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
    def last_update(self):
        return self._last_update

    @last_update.setter
    def last_update(self, last_update):
        self._last_update = last_update

    @property
    def seen(self):
        return self._seen

    @seen.setter
    def seen(self, seen):
        self._seen = seen

    def __str__(self):
        """ Overloads str method. """
        return 'Request(req_id = ' + str(self.req_id) + ', tid = ' + str(self.tid) + ', uid = ' + str(self.uid) \
               + ', sid = ' + str(self.sid) + ', create_date = ' + str(self.create_date) + ', last_update = ' \
               + str(self._last_update) + ', seen = ' + str(self.seen) + ')'
