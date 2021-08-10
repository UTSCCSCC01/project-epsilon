from databaseAccess.DAO import DAO
from databaseAccess.DAOCompanyPic import DAOCompanyPic
from flask_mysqldb import MySQL

def add_cpic(mysql:MySQL, tid:int, file) -> str:
    dao_pic = DAOCompanyPic(mysql)
    try:
        dao_pic.add_cpic(tid,file)
        return "File uploaded"
    except Exception as e:
        return e

def get_cpic(mysql:MySQL, tid:int):
    dao_pic = DAOCompanyPic(mysql)
    try:
        return dao_pic.get_cpic(tid)
    except Exception as e:
        raise e

def edit_cpic(mysql:MySQL, tid:int, file) -> str:
    dao_pic = DAOCompanyPic(mysql)
    try:
        dao_pic.edit_cpic(tid,file)
        return "File altered"
    except Exception as e:
        return e