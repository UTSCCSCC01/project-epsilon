from flask import Flask
from flask_mysqldb import MySQL
from datetime import datetime

def populate(mysql):
    # Create a table with 5 users. 2 admin and 3 normal users
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (uid INTEGER, role INTEGER)''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Teams (tid INTEGER, uid INTEGER, role INTEGER)''')
    cur.execute('''INSERT INTO Users VALUES (1, 1)''')
    cur.execute('''INSERT INTO Users VALUES (2, 1)''')
    cur.execute('''INSERT INTO Users VALUES (3, 0)''')
    cur.execute('''INSERT INTO Users VALUES (4, 0)''')
    cur.execute('''INSERT INTO Users VALUES (5, 0)''')
    mysql.connection.commit()
    return

def add_data(mysql, sql_q, data):
    # Adds data to table.
    cur = mysql.connection.cursor()
    cur.execute(sql_q, data)
    mysql.connection.commit()
    return "Added data successfully."

def populate2(mysql):
    # Add Primary Key Constraints and Foreign Key Constraints
    # Create more tables and insert some records for each table
    cur = mysql.connection.cursor()

    # Tables creation and Adding constraints to existing tables
    # cur.execute('''CREATE TABLE IF NOT EXISTS Company (tid INTEGER, name VARCHAR(200), description VARCHAR(200), creation_date DATETIME, PRIMARY KEY(tid))''')
    cur.execute("CREATE TABLE IF NOT EXISTS Company (" 
                "tid INTEGER, "
                "name VARCHAR(255), "
                "description VARCHAR(255), "
                "creation_date DATETIME, "
                "PRIMARY KEY(tid)"
                ")")
    # Use RStatus as status is a keyword
    cur.execute("CREATE TABLE IF NOT EXISTS RStatus ("
                "sid INTEGER,"
                "name VARCHAR(255),"
                "PRIMARY KEY(sid)"
                ")")
    cur.execute("CREATE TABLE IF NOT EXISTS Roles ("
                "rid INTEGER,"
                "name VARCHAR(255),"
                "PRIMARY KEY(rid)"
                ")")
    cur.execute("ALTER TABLE Users "
                "ADD PRIMARY KEY(uid)")
    cur.execute("ALTER TABLE Teams "
                "ADD FOREIGN KEY(tid) REFERENCES Company(tid), "
                "ADD FOREIGN KEY(uid) REFERENCES Users(uid), "
                "ADD FOREIGN KEY(role) REFERENCES Roles(rid),"
                "ADD CONSTRAINT PK_Teams PRIMARY KEY(tid, uid)")

    cur.execute("CREATE TABLE IF NOT EXISTS Request ("
                "req_id INTEGER,"
                "tid INTEGER, "
                "uid INTEGER, "
                "sid INTEGER, "
                "creation_date DATETIME,"
                "last_update TIMESTAMP,"
                "seen BOOLEAN,"
                "PRIMARY KEY(req_id),"
                "FOREIGN KEY(tid) REFERENCES Company(tid),"
                "FOREIGN KEY(uid) REFERENCES Users(uid),"
                "FOREIGN KEY(sid) REFERENCES RStatus(sid)"
                ")")

    #Adding records
    add_data(mysql, '''INSERT INTO Roles VALUES (%s, %s)''', (1,"Team Owner"))
    add_data(mysql, '''INSERT INTO Roles VALUES (%s, %s)''', (2,"Team Admin"))
    add_data(mysql, '''INSERT INTO Roles VALUES (%s, %s)''', (3,"Team Member"))

    add_data(mysql, '''INSERT INTO Company VALUES (%s, %s, %s, %s)''', (1,"Epsilon", "A startup named Epsilon.", datetime.now()))
    add_data(mysql, '''INSERT INTO Company VALUES (%s, %s, %s, %s)''', (2,"Delta", "A startup named Delta.", datetime.now()))
    
    add_data(mysql, '''INSERT INTO Teams VALUES (%s, %s, %s)''', (1,1,1))
    add_data(mysql, '''INSERT INTO Teams VALUES (%s, %s, %s)''', (2,2,1))

    add_data(mysql, '''INSERT INTO RStatus VALUES (%s, %s)''', (1,"Accepted"))
    add_data(mysql, '''INSERT INTO RStatus VALUES (%s, %s)''', (2,"Rejected"))
    add_data(mysql, '''INSERT INTO RStatus VALUES (%s, %s)''', (3,"Pending"))

    add_data(mysql, '''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (1,1,3,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), False))
    add_data(mysql, '''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (2,1,4,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), True))
    add_data(mysql, '''INSERT INTO Request VALUES (%s, %s, %s, %s, %s, %s, %s)''', (3,2,5,3,datetime.now(), datetime.now().strftime('%Y-%m-%d %H:%M:%S'), True))


    mysql.connection.commit()
    return