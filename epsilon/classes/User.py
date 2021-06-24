class User:
    def __init__(self, uid=0, rid=0, name="", contact=""):
        self._uid = uid
        self._rid = rid
        self._name = name
        self._contact = contact

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

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, contact):
        self._contact = contact

    def __str__(self):
        return 'User(uid = ' + str(self.uid) + ', rid = ' + str(self.rid) + ', name = ' \
               + self.name + ', contact = ' + self.contact + ')'