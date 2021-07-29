class Service:
    def __init__(self, ser_id=0, uid=0, ser_type_id=0, title="", description="", price=0, link=""):
        self._ser_id = ser_id
        self._uid = uid
        self._ser_type_id = ser_type_id
        self._title = title
        self._description = description
        self._price = price
        self._link = link

    @property
    def ser_id(self):
        return self._ser_id

    @ser_id.setter
    def ser_id(self, ser_id):
        self._ser_id = ser_id

    @property
    def uid(self):
        return self._uid

    @uid.setter
    def uid(self, uid):
        self._uid = uid

    @property
    def ser_type_id(self):
        return self._ser_type_id

    @ser_type_id.setter
    def ser_type_id(self, ser_type_id):
        self._ser_type_id = ser_type_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price):
        self._price = price

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link):
        self._link = link

    def __str__(self):
        """ Overloads str method. """
        return 'Service(ser_id = ' + str(self.ser_id) \
            + ', uid = ' + str(self.uid) \
            + ', ser_type_id = ' + str(self.ser_type_id) \
            + ', title = ' + self.title \
            + ', description = ' + self.description \
            + ', price = ' + str(self.price)\
            + ', link = ' + self.link + ')'
