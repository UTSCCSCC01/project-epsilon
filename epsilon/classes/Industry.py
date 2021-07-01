class Industry:
    def __init__(self, ind_id=0, name=""):
        self._ind_id = ind_id
        self._name = name

    @property
    def ind_id(self):
        return self._ind_id

    @ind_id.setter
    def ind_id(self, ind_id):
        self._ind_id = ind_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __str__(self):
        """ Overloads str method. """
        return 'Industry(ind_id = ' + str(self.ind_id) + ', name = ' + str(self.name) + ')'
