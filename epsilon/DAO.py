from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime

from epsilon.classes.Company import Company
from epsilon.classes.RStatus import RStatus
from epsilon.classes.Request import Request
from epsilon.classes.Role import Role
from epsilon.classes.Team import Team
from epsilon.classes.User import User


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
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (uid INTEGER, rid INTEGER, 
            name VARCHAR (50), contact VARCHAR (50))''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Teams (tid INTEGER, uid INTEGER, rid INTEGER)''')
        cur.execute("CREATE TABLE IF NOT EXISTS Roles ("
                    "rid INTEGER,"
                    "role_type VARCHAR(255),"
                    "PRIMARY KEY(rid)"
                    ")")
        cur.execute("CREATE TABLE IF NOT EXISTS RStatus ("
                    "sid INTEGER,"
                    "name VARCHAR(255),"
                    "PRIMARY KEY(sid)"
                    ")")
        cur.execute("CREATE TABLE IF NOT EXISTS Request ("
                    "req_id INTEGER,"
                    "tid INTEGER, "
                    "uid INTEGER, "
                    "sid INTEGER, "
                    "create_date DATETIME,"
                    "last_update TIMESTAMP,"
                    "seen BOOLEAN,"
                    "PRIMARY KEY(req_id)"
                    ")")
        cur.execute("ALTER TABLE Users "
                    "ADD PRIMARY KEY(uid),"
                    "ADD FOREIGN KEY(rid) REFERENCES Roles(rid)"
                    )
        cur.execute("ALTER TABLE Teams "
                    "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                    "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                    "ADD FOREIGN KEY(rid) REFERENCES Roles(rid),"
                    "ADD CONSTRAINT PK_Teams PRIMARY KEY(tid, uid)")

        cur.execute("ALTER TABLE Request "
                    "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                    "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                    "ADD FOREIGN KEY(sid) REFERENCES RStatus(sid)")

        cur.close()

        # uid, rid, name, contact
        paula = User(1, 1, "Paula", "ok@gmail.com")
        tim = User(2, 1, "Tim", "ko@gmail.com")
        pritish = User(3, 0, "Pritish", "lp@gmail.com")
        sam = User(4, 0, "Sam", "opll@gmail.com")
        water = User(5, 0, "Water", "no@gmail.com")
        users_to_add = [paula, tim, pritish, sam, water]

        # rid, role_type
        no_team = Role(0, "No Team")
        team_owner = Role(1, "Team Owner")
        team_admin = Role(2, "Team Admin")
        team_member = Role(3, "Team Member")
        roles_to_add = [no_team, team_owner, team_admin, team_member]

        # tid, uid, rid
        team_1 = Team(1, 1, 1)
        team_2 = Team(2, 2, 2)
        teams_to_add = [team_1, team_2]

        # tid, name, description, create_date
        epsilon = Company(1, "Epsilon", "A startup named Epsilon.", datetime.now())
        delta = Company(2, "Delta", "A startup named Delta.", datetime.now())
        companies_to_add = [epsilon, delta]

        # sid, name
        accepted = RStatus(1, "Accepted")
        rejected = RStatus(2, "Rejected")
        pending = RStatus(3, "Pending")
        r_status_to_add = [accepted, rejected, pending]

        # req_id, tid, uid, sid, create_date, last_update, seen
        request_1 = Request(1, 1, 3, 3, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0)
        request_2 = Request(2, 1, 4, 3, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
        request_3 = Request(3, 2, 5, 3, datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1)
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
        except:
            pass

    def get_data(self, sql_q, data):
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q, data)
            data = cur.fetchall()
            cur.close()
            return data
        except:
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
        except:
            pass

    # Add methods
    def add_company(self, company: Company):
        self.modify_data(
            '''INSERT INTO Company (tid, name, description, create_date) VALUES (%s, %s, %s, %s)''',
            (company.tid, company.name, company.description, company.create_date)
        )

    def add_request(self, request: Request):
        print(request)
        self.modify_data(
            '''INSERT INTO Request (req_id, tid, uid, sid, create_date, last_update, seen) VALUES (%s, %s, %s, %s, 
            %s, %s, %s)''',
            (request.req_id, request.tid, request.uid, request.sid, request.create_date, request.last_update, request.seen)
        )

    def add_role(self, role: Role):
        self.modify_data(
            '''INSERT INTO Roles (rid, role_type) VALUES (%s, %s)''',
            (role.rid, role.role_type)
        )

    def add_r_status(self, r_status: RStatus):
        self.modify_data(
            '''INSERT INTO RStatus (sid, name) VALUES (%s, %s)''',
            (r_status.sid, r_status.name)
        )

    def add_team(self, team: Team):
        self.modify_data(
            '''INSERT INTO Teams (tid, uid, rid) VALUES (%s, %s, %s)''',
            (team.tid, team.uid, team.rid)
        )

    def add_user(self, user: User):
        self.modify_data(
            '''INSERT INTO Users (uid, rid, name, contact) VALUES (%s, %s, %s, %s)''',
            (user.uid, user.rid, user.name, user.contact)
        )

    # Update methods
    def update_role_of_employee(self, uid, newRole):
        self.modify_data('''UPDATE Teams SET rid=%s WHERE uid=%s ''', (newRole, uid))
        self.modify_data('''UPDATE Users SET rid=%s WHERE uid=%s ''', (newRole, uid))

    # Remove methods
    def remove_team(self, tid, uid):
        self.modify_data('''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''', (tid, uid))

    # Get methods
    def retrieve_team(self, tid):
        team = None
        data = self.get_data('''SELECT FROM Teams WHERE tid = %s''', tid)
        if data.len() == 1:
            team = data[0]
            team = Team(team[0], team[1], team[2])
        return team

    def get_companies(self):
        companies = []
        data = self.get_data('''SELECT * FROM Company''', None)
        for company in data:
            companies.append(Company(company[0], company[1], company[2], company[3]))
        return companies

    def get_users(self):
        users = []
        data = self.get_data('''SELECT * FROM Users''', None)
        for user in data:
            users.append(User(user[0], user[1], user[2], user[3]))
        return users

    def get_teams(self):
        teams = []
        data = self.get_data('''SELECT * FROM Teams''', None)
        for team in data:
            teams.append(Team(team[0], team[1], team[2]))
        return teams

    def get_roles(self):
        roles = []
        data = self.get_data('''SELECT * FROM Roles''', None)
        for role in data:
            roles.append(Role(role[0], role[1]))
        return roles
