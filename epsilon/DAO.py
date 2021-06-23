
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime

class DAO:
    def __init__(self, db):
        self.db = db

    def populate(self):
        # Create a table with 5 users. 2 admin and 3 normal users
        cur = self.db.connection.cursor()
        cur.execute(
        '''CREATE TABLE IF NOT EXISTS Company (
	    tid int auto_increment,
	    name text not null,
	    description text not null,
	    create_date timestamp default current_timestamp null,
	    constraint Company_pk
	    primary key (tid));''')
        cur.execute('''CREATE TABLE IF NOT EXISTS Users (uid INTEGER, rid INTEGER, 
            name VARCHAR (50), contact VARCHAR (50))''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Teams (tid INTEGER, uid INTEGER, role INTEGER)''')
        cur.execute("CREATE TABLE IF NOT EXISTS Roles ("
                    "rid INTEGER,"
                    "type VARCHAR(255),"
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
                    "creation_date DATETIME,"
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
                    "ADD FOREIGN KEY(role) REFERENCES Roles(rid),"
                    "ADD CONSTRAINT PK_Teams PRIMARY KEY(tid, uid)")

        cur.execute("ALTER TABLE Request "
                    "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                    "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                    "ADD FOREIGN KEY(sid) REFERENCES RStatus(sid)")

        cur.close()

        # uid, rid, name, contact
        users_to_add = [(1, 1, "Paula", "ok@gmail.com"), (2, 1, "Tim", "ko@gmail.com"), (3, 0, "Pritish", "lp@gmail.com"),
                        (4, 0, "Sam", "opll@gmail.com"), (5, 0, "Water", "no@gmail.com")]
        # rid, type
        roles_to_add = [(0,"No Team"), (1,"Team Owner"), (2,"Team Admin"), (3,"Team Member")]
        # tid, uid, role
        teams_to_add = [(1, 1, 1), (2, 2, 1)]

        self.modify_data('''INSERT INTO Company VALUES (%s, %s, %s, %s)''', (1,"Epsilon", "A startup named Epsilon.", datetime.now()))
        self.modify_data('''INSERT INTO Company VALUES (%s, %s, %s, %s)''', (2,"Delta", "A startup named Delta.", datetime.now()))

        self.modify_data('''INSERT INTO RStatus VALUES (%s, %s)''', (1,"Accepted"))
        self.modify_data('''INSERT INTO RStatus VALUES (%s, %s)''', (2,"Rejected"))
        self.modify_data('''INSERT INTO RStatus VALUES (%s, %s)''', (3,"Pending"))

        for role in roles_to_add:
            self.modify_data('''INSERT INTO Roles (rid, type) VALUES (%s, %s)''', role)
        for user in users_to_add:
            self.modify_data('''INSERT INTO Users (uid, rid, name, contact) VALUES (%s, %s, %s, %s)''', user)
        for relation in teams_to_add:
            self.modify_data('''INSERT INTO Teams (tid, uid, role) VALUES (%s, %s, %s)''', relation)

        self.modify_data('''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (1,1,3,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0))
        self.modify_data('''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (2,1,4,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1))
        self.modify_data('''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (3,2,5,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 1))
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

    def updateRoleOfEmployee(self, uid, newRole):
        self.modify_data('''UPDATE Teams SET role=%s WHERE uid=%s ''', (newRole,uid))
        self.modify_data('''UPDATE Users SET rid=%s WHERE uid=%s ''', (newRole,uid))
    
    def removeTeam(self, tid, uid):
        self.modify_data('''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''',(tid,uid))

    def retrieveTeam(self, tid):
        team = self.get_data('''SELECT FROM Teams WHERE tid = %s''', (tid))
        return team

    def get_Companies(self):
        companies = self.get_data('''SELECT * FROM Company''', None)
        return companies

    def get_Users(self):
        users = self.get_data('''SELECT * FROM Users''', None)
        return users

    def get_Teams(self):
        teams = self.get_data('''SELECT * FROM Teams''', None)
        return teams

    def get_Roles(self):
        roles = self.get_data('''SELECT * FROM Roles''', None)
        return roles

    
