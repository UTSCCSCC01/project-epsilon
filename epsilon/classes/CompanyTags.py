class CompanyTags:
    def __init__(self, ctid=0, tid=0, tag_id=0):
        self._ctid = ctid
        self._tid = tid
        self._tag_id = tag_id

    @property
    def ctid(self):
        return self._ctid

    @ctid.setter
    def ctid(self, ctid):
        self._ctid = ctid

    @property
    def tid(self):
        return self._tid

    @tid.setter
    def tid(self, tid):
        self._tid = tid

    @property
    def tag_id(self):
        return self._tag_id

    @tag_id.setter
    def tag_id(self, tag_id):
        self._tag_id = tag_id

    def __str__(self):
        """ Overloads str method. """
        return 'CompanyTags(ctid = ' + str(self.ctid) + ', tid = ' + str(self.tid) + ', tag_id = ' \
               + str(self.tag_id) + ')'
