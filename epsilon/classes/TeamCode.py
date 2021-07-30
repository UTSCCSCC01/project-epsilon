class TeamCode:
    def __init__(self, tid=0, code="", create_time=""):
        self._tid = tid
        self._code = code
        self._create_time = create_time

    @property
    def tid(self):
        return self._tid
    
    @tid.setter
    def tid(self,tid):
        self._tid = tid

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self,code):
        self._code = code

    @property
    def create_time(self):
        return self._create_time

    @create_time.setter
    def create_time(self, create_time):
        self._create_time = create_time

    def __str__(self):
        """ Overload String method"""
        return 'TeamCode(tid = ' + str(self.tid) + \
                        'code =' + self.code + \
                        'create_time =' + self.create_time + \
                        ')' 