
from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime

def populate(mysql):
    # Create a table with 5 users. 2 admin and 3 normal users
    cur = mysql.connection.cursor()
    if not tables_exist(mysql):
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Company (
	            tid int auto_increment,
	            name text not null,
	            description text not null,
	            create_date timestamp default current_timestamp null,
	            constraint Company_pk
	            primary key (tid));''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Roles (
                rid INTEGER NOT NULL,
                type VARCHAR(255),
                PRIMARY KEY(rid));''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Users (
                uid INTEGER NOT NULL,
                rid INTEGER NOT NULL, 
                name VARCHAR (50), 
                contact VARCHAR (50),
                PRIMARY KEY(uid),
                FOREIGN KEY(rid) REFERENCES Roles(rid));''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Teams (
                tid INTEGER NOT NULL, 
                uid INTEGER NOT NULL, 
                rid INTEGER NOT NULL,
                CONSTRAINT PK_Teams PRIMARY KEY(tid, uid),
                FOREIGN KEY(tid) REFERENCES Company(tid),
                FOREIGN KEY(uid) REFERENCES Users(uid),
                FOREIGN KEY(rid) REFERENCES Roles(rid));''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS RStatus (
                sid INTEGER NOT NULL,
                name VARCHAR(255),
                PRIMARY KEY(sid));''')
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS Request (
                req_id INTEGER auto_increment,
                tid INTEGER, 
                uid INTEGER, 
                sid INTEGER, 
                create_date DATETIME,
                last_update TIMESTAMP default current_timestamp null,
                seen BOOLEAN,
                PRIMARY KEY(req_id),
                FOREIGN KEY(tid) REFERENCES Company(tid),
                FOREIGN KEY(uid) REFERENCES Users(uid),
                FOREIGN KEY(sid) REFERENCES RStatus(sid));''')
        #cur.execute("ALTER TABLE Users "
        #            "ADD PRIMARY KEY(uid),"
        #            "ADD FOREIGN KEY(rid) REFERENCES Roles(rid)"
        #            )
        #cur.execute("ALTER TABLE Teams "
        #            "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
        #            "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
        #            "ADD FOREIGN KEY(role) REFERENCES Roles(rid),"
        #            "ADD CONSTRAINT PK_Teams PRIMARY KEY(tid, uid)")

        #cur.execute("ALTER TABLE Request "
        #            "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
        #            "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
        #            "ADD FOREIGN KEY(sid) REFERENCES RStatus(sid)")
        mysql.connection.commit()

        insert_test_data(mysql)

        cur1 = mysql.connection.cursor()
        cur1.execute('''SELECT * FROM Users''')
        cur2 = mysql.connection.cursor()
        cur2.execute('''SELECT * FROM Teams''')
        cur3 = mysql.connection.cursor()
        cur3.execute('''SELECT * FROM Roles''')
        return "Tables Users, Teams, Roles are populated!\n" \
               "Also five dummy employees Paula, Tim, Pritish, Sam, Water."+"\n\n"\
               + str(cur1.fetchall())+"\n\n"+str(cur2.fetchall())\
               + "\n\n"+str(cur3.fetchall())

    return "Tables already exist!"

def insert_test_data(mysql):
    # uid, rid, name, contact
    users_to_add = [(1, 1, "Paula", "ok@gmail.com"), (2, 1, "Tim", "ko@gmail.com"), (3, 0, "Pritish", "lp@gmail.com"),
                    (4, 0, "Sam", "opll@gmail.com"), (5, 0, "Water", "no@gmail.com")]
    # rid, type
    roles_to_add = [(0,"No Team"), (1,"Team Owner"), (2,"Team Admin"), (3,"Team Member")]
    # tid, uid, role
    teams_to_add = [(1, 1, 1), (2, 2, 1)]

    # name, description
    companies_to_add = [("Epsilon", "A startup named Epsilon."), ("Delta", "A startup named Delta.")]

    # sid, name
    status_to_add = [(1,"Accepted"), (2,"Rejected"), (3,"Pending")]
    # tid, uid, sid, create_date, seen
    requests_to_add = [(1,3,3,datetime.now(), 0), (1,4,3,datetime.now(), 1), (2,5,3,datetime.now(), 1)]
    for role in roles_to_add:
        add_data(mysql, '''INSERT INTO Roles (rid, type) VALUES (%s, %s)''', role)
    for user in users_to_add:
        add_data(mysql, '''INSERT INTO Users (uid, rid, name, contact) VALUES (%s, %s, %s, %s)''', user)
    for company in companies_to_add:
        add_data(mysql, '''INSERT INTO Company (name, description) VALUES (%s, %s)''', company)
    for relation in teams_to_add:
        add_data(mysql, '''INSERT INTO Teams (tid, uid, rid) VALUES (%s, %s, %s)''', relation)
    for status in status_to_add:
        add_data(mysql, '''INSERT INTO RStatus VALUES (%s, %s)''', status)
    for request in requests_to_add:
        add_data(mysql, '''INSERT INTO Request (tid, uid, sid, create_date, seen) VALUES (%s, %s, %s, %s, %s)''', request)

    mysql.connection.commit()
    return None


def add_data(mysql, sql_q, data):
    # Adds data to table.
    try:
        cur = mysql.connection.cursor()
        cur.execute(sql_q, data)
        mysql.connection.commit()
        return "Done!"
    except:
        pass

def get_data(mysql, dbname):
    # Gets data from table = dbname
    cur = mysql.connection.cursor()
    sql_q = '''SELECT * FROM ''' + dbname
    cur.execute(sql_q)
    data = cur.fetchall()
    return data

def tables_exist(mysql):
    cur = mysql.connection.cursor()
    cur.execute('''SHOW TABLES''')
    result = cur.fetchone()
    return result