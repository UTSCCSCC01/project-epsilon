class Request:
    def __init__(self, req_id=0, tid=0, uid=0, sid=0, create_date="", last_update="", seen=-1):
        self.req_id = req_id
        self.tid = tid
        self.uid = uid
        self.sid = sid
        self.create_date = create_date
        self.last_update = last_update
        self.seen = seen
