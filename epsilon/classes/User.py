class User:
    def __init__(self, uid=0, rid=0, name="", contact="",description="", password=""):
        self._uid = uid
        self._rid = rid
        self._name = name
        self._contact = contact
        self.password = password
        self._description = description

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

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def description(self):
         return self._description

    @description.setter
    def description(self, description):
        self._description = description


    def __str__(self):
        """ Overloads str method. """
        return 'User(uid = ' + str(self.uid) \
            + ', rid = ' + str(self.rid) \
            + ', name = ' + self.name \
            + ', contact = ' + self.contact \
            + ', description = ' + self.description + ')'
