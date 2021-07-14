from flask_login import UserMixin
# rid is required for display team
class User(UserMixin):
    def __init__(self, uid=0, type_id=0, name="", contact="",
                 password="", description="", rid=0):
        self._uid = uid
        self._type_id = type_id
        self._name = name
        self._contact = contact
        self._description = description
        self._password = password
        self._rid = rid

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def type_id(self):
        return self._type_id

    @type_id.setter
    def type_id(self, type_id):
        self._type_id = type_id

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

    @property
    def rid(self):
        return self._rid

    @rid.setter
    def rid(self, rid):
        self._rid = rid

    def get_id(self):
        try:
            return str(self.uid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __str__(self):
        """ Overloads str method. """
        return 'User(uid = ' + str(self.uid) \
            + ', type_id = ' + str(self.type_id) \
            + ', name = ' + self.name \
            + ', contact = ' + self.contact \
            + ', pwd = ' + self.password\
            + ', description = ' + self.description + ')'
