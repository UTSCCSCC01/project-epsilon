from databaseAccess.DAO import DAO
from databaseAccess.DAOProfilePic import DAOProfilePic
from flask_mysqldb import MySQL

def add_pic(mysql:MySQL, uid:int, file) -> str:
    dao_pic = DAOProfilePic(mysql)
    try:
        dao_pic.add_pic(uid,file)
        return "File uploaded"
    except Exception as e:
        return e

def get_pic(mysql:MySQL, uid:int):
    dao_pic = DAOProfilePic(mysql)
    try:
        return dao_pic.get_pic(uid)
    except Exception as e:
        raise e

def edit_pic(mysql:MySQL, uid:int, file) -> str:
    dao_pic = DAOProfilePic(mysql)
    try:
        dao_pic.edit_pic(uid,file)
        return "File altered"
    except Exception as e:
        return e