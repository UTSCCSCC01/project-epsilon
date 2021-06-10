def populate(mysql):
    # Create a table with 5 users. 2 admin and 3 normal users
    cur = mysql.connection.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS Users (uid INTEGER, role INTEGER)''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Teams (tid INTEGER, uid INTEGER, role INTEGER)''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS Company (
	tid int auto_increment,
	name text not null,
	description text not null,
	create_date timestamp default current_timestamp null,
	constraint Company_pk
	primary key (tid)
    );''')
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
    return "Done!"

def get_data(mysql, dbname):
    # Gets data from table = dbname
    cur = mysql.connection.cursor()
    sql_q = '''SELECT * FROM ''' + dbname
    cur.execute(sql_q)
    data = cur.fetchall()
    return data