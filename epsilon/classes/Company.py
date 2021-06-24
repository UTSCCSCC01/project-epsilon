class Company:
    def __init__(self, tid=0, name="", description="", create_date=""):
        self._tid = tid
        self._name = name
        self._description = description
        self._create_date = create_date

    @property
    def tid(self):
        return self._tid

    @tid.setter
    def tid(self, tid):
        self._tid = tid

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def create_date(self):
        return self._create_date

    @create_date.setter
    def create_date(self, create_date):
        self._create_date = create_date
