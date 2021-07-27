from datetime import datetime
from typing import List
from .DAO import DAO
from classes.RStatus import RStatus
from classes.Request import Request


class DAORequest(DAO):
    # child class of DAO.
    # contains database access methods related to role.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_request_table(self) -> None:
        """
        Creates the request table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS Request ("
                        "req_id INTEGER auto_increment,"
                        "tid INTEGER, "
                        "uid INTEGER, "
                        "sid INTEGER, "
                        "create_date DATETIME default current_timestamp null,"
                        "last_update TIMESTAMP default current_timestamp "
                        "ON UPDATE CURRENT_TIMESTAMP,"
                        "seen BOOLEAN,"
                        "PRIMARY KEY(req_id)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Company, Users and RStatus tables to be created.
        """
        super().add_foreign_key("Request", "tid", "Company")
        super().add_foreign_key("Request", "uid", "Users")
        super().add_foreign_key("Request", "sid", "RStatus")

    def add_dummy_requests(self) -> None:
        """
        Populate request table with dummy data.
        Require: Company and user to have dummy objects.
                 RStatus to be populated.
        """
        request_1 = Request(req_id=1, tid=1, uid=3,
                            sid=RStatus.OFFER.value,
                            create_date=datetime.now(),
                            last_update=datetime.now()
                            .strftime('%Y-%m-%d %H:%M:%S'),
                            seen=0)
        request_2 = Request(req_id=2, tid=1, uid=4,
                            sid=RStatus.OFFER.value,
                            create_date=datetime.now(),
                            last_update=datetime.now()
                            .strftime('%Y-%m-%d %H:%M:%S'),
                            seen=1)
        request_3 = Request(req_id=3, tid=2, uid=5,
                            sid=RStatus.OFFER.value,
                            create_date=datetime.now(),
                            last_update=datetime.now()
                            .strftime('%Y-%m-%d %H:%M:%S'),
                            seen=1)
        requests_to_add = [request_1, request_2, request_3]

        for request in requests_to_add:
            self.add_request(request)

    def add_request(self, request: Request) -> None:
        """
        Adds a new request into the database.
        :param request: A Request object representing the request to be added.
        """
        self.modify_data(
            '''INSERT INTO Request (tid, uid, sid, seen)
            VALUES (%s, %s, %s, %s)''',
            (request.tid,
             request.uid,
             request.sid,
             request.seen))

    def update_request(self, request: Request) -> None:
        """
        Updates an existing request.
        :param request: A Request object representing the
                        request to be updated.
        """
        self.modify_data(
            '''UPDATE Request Set sid = %s, seen = false WHERE req_id = %s''',
            (request.sid, request.req_id))

    def get_requests_by_uid(self, uid: int) -> List[Request]:
        """
        Gets all requests for user with uid from the database.
        :param req_id: request id of the request to be retrieved.
        :return: request object representing the matching request.
                 None if not found.
        """
        requests = []
        data = self.get_data('''SELECT * FROM Request
                                WHERE uid = %s
                                ORDER BY create_date DESC''',
                             (uid,))
        for request in data:
            requests.append(Request(request[0], request[1], request[2],
                                    request[3], request[4], request[5],
                                    request[6]))
        return requests

    def get_request_by_req_id(self, req_id: int) -> Request:
        """
        Gets a request from the database.
        :param req_id: request id of the request to be retrieved.
        :return: request object representing the matching request.
                 None if not found.
        """
        request = None
        data = self.get_data('''SELECT *
                             FROM Request WHERE req_id = %s''', (req_id,))
        if data is not None:
            request = data[0]
            request = Request(request[0], request[1], request[2],
                              request[3], request[4], request[5],
                              request[6])
        return request

    def get_requests_by_tid_sid(self, tid: int, sid: int) -> List[Request]:
        """
        Gets all pending requests for team with tid from the database.
        :param tid: Team id of the requests to be retrieved.
        :param sid: Status id of requests wanted.
        :return: List of Request objects representing
                 the matching team and status.
        """
        requests = []
        data = self.get_data('''SELECT * FROM Request
                                WHERE tid = %s AND sid = %s
                                ORDER BY create_date''',
                             (tid, sid))
        for request in data:
            requests.append(Request(request[0], request[1], request[2],
                                    request[3], request[4], request[5],
                                    request[6]))
        return requests

    def get_requests_by_tid_uid_sid(self, tid: int, uid: int, sid: int) -> List[Request]:
        """
        Gets all pending requests for team with tid from the database.
        :param tid: Team id of the requests to be retrieved.
        :param sid: Status id of requests wanted.
        :return: List of Request objects representing
                 the matching team and status.
        """
        requests = []
        data = self.get_data('''SELECT * FROM Request
                                WHERE tid = %s AND uid = %s AND sid=%s
                                ORDER BY create_date''',
                             (tid, uid, sid))
        for request in data:
            requests.append(Request(request[0], request[1], request[2],
                                    request[3], request[4], request[5],
                                    request[6]))
        return requests