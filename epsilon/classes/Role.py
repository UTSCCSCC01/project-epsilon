class Role:
    def __init__(self, rid=0, role_type=""):
        self._rid = rid
        self._role_type = role_type

    @property
    def rid(self):
        return self._rid

    @rid.setter
    def rid(self, rid):
        self._rid = rid

    @property
    def role_type(self):
        return self._role_type

    @role_type.setter
    def role_type(self, role_type):
        self._role_type = role_type
