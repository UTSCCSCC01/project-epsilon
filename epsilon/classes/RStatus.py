class RStatus:
    def __init__(self, sid=0, name=""):
        self._sid = sid
        self._name = name

    @property
    def sid(self):
        return self._sid

    @sid.setter
    def sid(self, sid):
        self._sid = sid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
