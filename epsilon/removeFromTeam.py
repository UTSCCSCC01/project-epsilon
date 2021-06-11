from flask import Flask
from flask_mysqldb import MySQL
from populatedatabase import add_data

# ask kobe if this should be its own thing or if it should piggy back off his add data
# def updateData(mysql, sql_q, data):

def removeFromTeam(mysql, uid, tid):
    cur = mysql.connection.cursor()
    # replace 1s with references to real user data
    cur.execute('''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''',(tid,uid))
    mysql.connection.commit()

def retrieveTeam(mysql,tid):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT FROM Teams WHERE tid = %s''', (tid))
    out = cur.fetchall()
    ret = []
    for x in out:
        x.replace('(','')
        x.replace(')','')
        x.replace('\'','')
        x.replace(' ','')
        ret.append(x.split(','))
    return ret
    # replace 1s with references to real user data


def updateRoleOfEmployee(mysql, uid, rid):
    # cur.execute(sql_q, data)
    add_data(mysql, '''UPDATE Users SET rid=%s WHERE uid=%s ''', (rid,uid))
    # cur = mysql.connection.cursor()
    # cur.execute('''SELECT FROM Roles WHERE rid = %s''', (rid))
    # res = cur.fetchall()
    # if (len(res) != 0):
    #     role = res[0]
    # add_data(mysql, '''UPDATE Users SET =%s WHERE uid=%s ''', (rid, uid))