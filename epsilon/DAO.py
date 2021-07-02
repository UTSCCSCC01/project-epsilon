from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime

from classes.Company import Company
from classes.RStatus import RStatus
from classes.Request import Request
from classes.Role import Role
from classes.Team import Team
from classes.User import User


class DAO:
    def __init__(self, db):
        self.db = db

    def populate(self):
        # Create a table with 5 users. 2 admin and 3 normal users
        cur = self.db.connection.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Company (
                    tid int auto_increment,
                    name text not null,
                    description text not null,
                    create_date timestamp default current_timestamp null,
                    constraint Company_pk
                    primary key (tid));''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                    uid INTEGER auto_increment,
                    rid INTEGER,
                    name text not null,
                    contact text not null,
                    password text not null,
                    constraint Users_pk
                    primary key (uid))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Teams (
                    tid INTEGER,
                    uid INTEGER,
                    rid INTEGER,
                    CONSTRAINT PK_Teams
                    PRIMARY KEY(tid, uid))''')
        cur.execute("CREATE TABLE IF NOT EXISTS Roles ("
                    "rid INTEGER,"
                    "role_type text not null,"
                    "PRIMARY KEY(rid)"
                    ")")
        cur.execute("CREATE TABLE IF NOT EXISTS RStatus ("
                    "sid INTEGER,"
                    "name text not null,"
                    "PRIMARY KEY(sid)"
                    ")")
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
        cur.execute("ALTER TABLE Users "
                    "ADD FOREIGN KEY(rid) REFERENCES Roles(rid)"
                    )
        cur.execute("ALTER TABLE Teams "
                    "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                    "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                    "ADD FOREIGN KEY(rid) REFERENCES Roles(rid)")

        cur.execute("ALTER TABLE Request "
                    "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                    "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                    "ADD FOREIGN KEY(sid) REFERENCES RStatus(sid)")

        cur.close()

        # uid, rid, name, contact
        # TODO: change role to type here
        paula = User(1, Role.TEAM_OWNER.value, "Paula", "ok@gmail.com", "admin")
        tim = User(2, Role.TEAM_OWNER.value, "Tim", "ko@gmail.com", "admin")
        pritish = User(3, Role.NO_TEAM.value, "Pritish", "lp@gmail.com", "admin")
        sam = User(4, Role.NO_TEAM.value, "Sam", "opll@gmail.com", "admin")
        water = User(5, Role.NO_TEAM.value, "Water", "no@gmail.com", "admin")
        users_to_add = [paula, tim, pritish, sam, water]

        # rid, role_type
        roles_to_add = [Role.NO_TEAM, Role.TEAM_OWNER, Role.TEAM_ADMIN, Role.TEAM_MEMBER]

        # tid, uid, rid
        team_1 = Team(1, 1, 1)
        team_2 = Team(2, 2, 1)
        teams_to_add = [team_1, team_2]

        # tid, name, description, create_date
        epsilon = Company(
            1,
            "Epsilon",
            "A startup named Epsilon.",
            datetime.now())
        delta = Company(2, "Delta", "A startup named Delta.", datetime.now())
        companies_to_add = [epsilon, delta]

        # sid, name
        r_status_to_add = [RStatus.ACCEPTED, RStatus.REJECTED, RStatus.PENDING]

        # req_id, tid, uid, sid, create_date, last_update, seen
        request_1 = Request(1, 1, 3, RStatus.PENDING.value, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0)
        request_2 = Request(2, 1, 4, RStatus.PENDING.value, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
        request_3 = Request(3, 2, 5, RStatus.PENDING.value, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
        requests_to_add = [request_1, request_2, request_3]

        for company in companies_to_add:
            self.add_company(company)

        for r_status in r_status_to_add:
            self.add_r_status(r_status)

        for role in roles_to_add:
            self.add_role(role)

        for user in users_to_add:
            self.add_user(user)

        for team in teams_to_add:
            self.add_team(team)

        for request in requests_to_add:
            self.add_request(request)

        self.db.connection.commit()

    def modify_data(self, sql_q, data):
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q, data)
            self.db.connection.commit()
            cur.close()
        except BaseException:
            pass

    def get_data(self, sql_q, data):
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q, data)
            data = cur.fetchall()
            cur.close()
            return data
        except BaseException:
            pass

    def delete_all(self):
        try:
            cur = self.db.connection.cursor()
            cur.execute('''DROP TABLE IF EXISTS Teams''')
            cur.execute('''DROP TABLE IF EXISTS Request''')
            cur.execute('''DROP TABLE IF EXISTS Users''')
            cur.execute('''DROP TABLE IF EXISTS Roles''')
            cur.execute('''DROP TABLE IF EXISTS Company''')
            cur.execute('''DROP TABLE IF EXISTS RStatus''')
            self.db.connection.commit()
            cur.close()
        except BaseException:
            pass

    # Add methods
    def add_company(self, company: Company):
        """
        Adds a new company into the database.
        :param company: A Company object representing the company to be added.
        """
        self.modify_data(
            '''INSERT INTO Company (name, description) VALUES (%s, %s)''',
            (company.name,
             company.description))

    def add_request(self, request: Request):
        """
        Adds a new request into the database.
        :param request: A Request object representing the request to be added.
        """
        self.modify_data(
            '''INSERT INTO Request (tid, uid, sid, seen) VALUES (%s, %s, %s,
            %s)''',
            (request.tid,
             request.uid,
             request.sid,
             request.seen))

    def add_role(self, role: Role):
        """
        Adds a new role into the database.
        :param role: A Role object representing the role to be added.
        """
        self.modify_data(
            '''INSERT INTO Roles (rid, role_type) VALUES (%s, %s)''',
            (role.value, role.name)
        )

    def add_r_status(self, r_status: RStatus):
        """
        Adds a new r_status into the database.
        :param r_status: A RStatus object representing the r_status to be added.
        """
        self.modify_data(
            '''INSERT INTO RStatus (sid, name) VALUES (%s, %s)''',
            (r_status.value, r_status.name)
        )

    def add_team(self, team: Team):
        """
        Adds a new team into the database.
        :param team: A Team object representing the team to be added.
        """
        self.modify_data(
            '''INSERT INTO Teams (tid, uid, rid) VALUES (%s, %s, %s)''',
            (team.tid, team.uid, team.rid)
        )

    def add_user(self, user: User):
        """
        Adds a new user into the database.
        :param user: A User object representing the user to be added.
        """
        self.modify_data(
            '''INSERT INTO Users (rid, name, contact, password) VALUES (%s, %s, %s, %s)''',
            (user.rid, user.name, user.contact, user.password)
        )

    # Update methods
    def update_role_of_employee(self, uid, new_rid):
        """
        Updates the role id of an employee in the database to new_rid.
        :param uid: User id of the employee.
        :param new_rid: New role id of the employee.
        """
        self.modify_data(
            '''UPDATE Teams SET rid=%s WHERE uid=%s ''', (new_rid, uid))
        self.modify_data(
            '''UPDATE Users SET rid=%s WHERE uid=%s ''', (new_rid, uid))

    def update_request_status(self, req_id, new_sid):
        """
        Updates the sid and seen of a request in
        the database to new_sid and true.
        :param uid: req_id of the request.
        :param new_sid: New status id of the request.
        """
        self.modify_data(
            '''UPDATE Request Set sid = %s, seen = true WHERE req_id = %s''',
            (new_sid, req_id))

    # Remove methods
    def remove_from_team(self, tid, uid):
        """
        Removes an employee from a team in the database.
        :param tid: team id of the employee to be removed.
        :param uid: user id of the employee to be removed.
        """
        self.modify_data(
            '''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''', (tid, uid))
        self.modify_data('''UPDATE Users SET rid=%s WHERE uid=%s ''', (0, uid))

    # Get methods
    def get_team(self, tid):
        """
        Gets a team from the database.
        :param tid: Team id of the team to be retrieved.
        :return: Team object representing the matching team. None if not found.
        """
        team = None
        data = self.get_data('''SELECT * FROM Teams WHERE tid = %s''', (tid,))
        if data is not None:
            team = data[0]
            team = Team(team[0], team[1], team[2])
        return team

    def get_companies(self):
        """
        Gets all companies in the database.
        :return: List of Company objects.
        """
        companies = []
        data = self.get_data('''SELECT * FROM Company''', None)
        for company in data:
            companies.append(
                Company(
                    company[0],
                    company[1],
                    company[2],
                    company[3]))
        return companies

    def get_users(self):
        """
        Gets all users in the database.
        :return: List of User objects.
        """
        users = []
        data = self.get_data('''SELECT * FROM Users''', None)
        for user in data:
            users.append(User(user[0], user[1], user[2], user[3], user[4]))
        return users

    def get_teams(self):
        """
        Gets all teams in the database.
        :return: List of Team objects.
        """
        teams = []
        data = self.get_data('''SELECT * FROM Teams''', None)
        for team in data:
            teams.append(Team(team[0], team[1], team[2]))
        return teams

    def get_roles(self):
        """
        Gets all roles in the database.
        :return: List of Role objects.
        """
        roles = []
        data = self.get_data('''SELECT * FROM Roles''', None)
        for role in data:
            roles.append(Role(role[0]))
        return roles

    
    def get_role(self, rid):
        """
        Gets a role from the database.
        :param rid: Role id of the role to be retrieved.
        :return: Role object representing the rid. None if not found.
        """
        role = None
        data = self.get_data('''SELECT * FROM Roles WHERE rid = %s''', (rid,))
        if data is not None:
            role = data[0]
        return Role(role[0])

    def get_users_from_team(self, tid):
        """
        Gets all users in a team.
        :param tid: Team id of the users to be retrieved.
        :return: list of users objects representing the matching team.
        """
        users = []
        data = self.get_data(
            '''SELECT users.uid, users.rid, users.name, users.contact, users.password
                        FROM epsilon_db.users JOIN epsilon_db.teams
                        ON users.uid = teams.uid
                        WHERE tid = %s''', (tid,))

        for user in data:
            users.append(User(user[0], user[1], user[2], user[3], user[4]))
        return users

    def get_pending_requests(self, tid):
        """
        Gets all pending requests for team with tid from the database.
        :param tid: Team id of the requests to be retrieved.
        :return: List of Request objects representing the matching team.
        """
        requests = []
        data = self.get_data('''SELECT * FROM Request WHERE tid = %s AND sid = 3 ORDER BY create_date''', (tid,))
        for request in data:
            requests.append(Request(request[0], request[1], request[2],
                                    request[3], request[4], request[5],
                                    request[6]))
        return requests

    def get_request(self, req_id):
        """
        Gets a request from the database.
        :param req_id: request id of the request to be retrieved.
        :return: request object representing the matching request. None if not found.
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

    def get_user(self, email):
        """
        Gets a user from the database.
        :param email: Email of the user to be retrieved.
        :return: User object representing the matching User. None if not found.
        """
        user = None
        data = self.get_data('''SELECT * FROM Users WHERE contact = %s''', (email,))
        if data:
            user = data[0]
            user = User(user[0], user[1], user[2], user[3], user[4])
        return user

    def get_company(self, name):
        """
        Gets a company from the database.
        :param name: name of the company to be retrieved.
        :return: Company object representing the matching Company. None if not found.
        """
        company = None
        data = self.get_data('''SELECT * FROM Company WHERE name = %s''', (name,))
        if data:
            company= data[0]
            company = Company(company[0], company[1], company[2], company[3])
        return company
