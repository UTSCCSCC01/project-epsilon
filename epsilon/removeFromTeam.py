from flask import Flask
from flask_mysqldb import MySQL
from DAO import DAO


# ask kobe if this should be its own thing or if it should piggy back off his add data
# def updateData(mysql, sql_q, data):

def remove_from_team(dao, uid, tid):
    dao.update_role_of_employee(uid, 0)
    dao.remove_team(tid, uid)


def retrieve_team(dao, tid):
    team = dao.retrieve_team(tid)
    return team
    # replace 1s with references to real user data
