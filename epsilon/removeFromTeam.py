from flask import Flask
from flask_mysqldb import MySQL
from DAO import DAO

# ask kobe if this should be its own thing or if it should piggy back off his add data
# def updateData(mysql, sql_q, data):

def removeFromTeam(dao, uid, tid):
    dao.updateRoleOfEmployee(uid, 0)
    dao.removeTeam(tid, uid)

def retrieveTeam(dao,tid):
    out = dao.retrieveTeam(tid)
    ret = []
    for x in out:
        x.replace('(','')
        x.replace(')','')
        x.replace('\'','')
        x.replace(' ','')
        ret.append(x.split(','))
    return ret
    # replace 1s with references to real user data
