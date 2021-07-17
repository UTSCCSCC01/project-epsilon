class Tag:
    def __init__(self, name="", ind_id=None, tag_id=0):
        self._name = name
        self._ind_id = ind_id
        self._tag_id = tag_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def ind_id(self):
        return self._ind_id

    @ind_id.setter
    def ind_id(self, ind_id):
        self._ind_id = ind_id

    @property
    def tag_id(self):
        return self._tag_id

    @tag_id.setter
    def tag_id(self, tag_id):
        self._tag_id = tag_id

    def __str__(self):
        """ Overloads str method. """
        return 'Tag(tag_id = ' + str(self.tag_id) + ', name = ' + str(self.name) + ', ind_id = ' \
               + str(self.ind_id) + ')'
