class TeamCode:
    def __init__(self, tid=0, code="", create_time=""):
        self.tid = tid
        self.code = code
        self.create_time = create_time

    @property
    def tid(self):
        return self.tid
    
    @tid.setter
    def tid(self,tid):
        self.tid = tid

    @property
    def code(self):
        return self.code

    @code.setter
    def code(self,code):
        self.code = code

    @property
    def create_time(self):
        return self.create_time

    @create_time.setter
    def create_time(self, create_time):
        self.create_time = create_time

    def __str__(self):
        """ Overload String method"""
        return 'TeamCode(tid = ' + str(self.tid) + \
                        'code =' + self.code + \
                        'create_time =' + self.create_time + \
                        ')' 