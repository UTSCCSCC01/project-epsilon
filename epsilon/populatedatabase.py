from flask import Flask
from flask_mysqldb import MySQL

def populate(mysql):
    # Create a table with 5 users. 2 admin and 3 normal users
    cur = mysql.connection.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Users (uid INTEGER, rid INTEGER, 
        name VARCHAR (50), contact VARCHAR (50))''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Teams (tid INTEGER, uid INTEGER)''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Roles (rid INTEGER, type VARCHAR (50))''')
    mysql.connection.commit()
    return


def populate3(mysql):
    # test displaying all employee list
    cur = mysql.connection.cursor()
    # uid, rid, name, contact
    users_to_add = [(1, 10, "Paula", "ok@gmail.com"), (2, 10, "Tim", "ko@gmail.com"), (3, 30, "Pritish", "lp@gmail.com"),
                    (4, 40, "Sam", "opll@gmail.com"), (5, 50, "Water", "no@gmail.com")]
    # rid, type
    roles_to_add = [(10, "admin"), (30, "CEO"), (40, "director"), (50, "scrum master")]
    # tid, uid
    teams_to_add = [(100, 1), (100, 2), (100, 3), (200, 4), (200, 5)]
    for user in users_to_add:
        add_data(mysql, '''INSERT INTO Users (uid, rid, name) VALUES (%s, %s,%s)''', user[:3])
    for role in roles_to_add:
        add_data(mysql, '''INSERT INTO Roles (rid, type) VALUES (%s, %s)''', role)
    for relation in teams_to_add:
        add_data(mysql, '''INSERT INTO Teams (tid, uid) VALUES (%s, %s)''', relation)
    mysql.connection.commit()
    return


def add_data(mysql, sql_q, data):
    # Adds data to table.
    cur = mysql.connection.cursor()
    cur.execute(sql_q, data)
    mysql.connection.commit()
    return "Added data successfully."
