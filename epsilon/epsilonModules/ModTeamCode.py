from classes.TeamCode import TeamCode
from flask_mysqldb import MySQL
from databaseAccess.DAOTeamCode import DAOTeamCode
import random, string

def codeActive(mysql:MySQL, tid:int) -> bool:
    """
    Checks if there is currently an active team code
    :param tid: company to search code for
    :param mysql: database in which code is found
    :return: whether the code is active or not
    """
    dao_teamCode = DAOTeamCode(mysql)
    # remove any teamCodes past autoexpiry timer
    dao_teamCode.remove_teamcodes()
    code = dao_teamCode.get_teamcode_by_tid(tid)
    if(code != None):
        return True
    return False

def checkCode(mysql:MySQL, code:str) -> bool:
    """
    See if code is valid 
    :param code: code to search for
    :param mysql: database in which code is found
    :return: whether the code is active or not
    """
    dao_teamCode = DAOTeamCode(mysql)
    teamCode = dao_teamCode.get_teamCode_by_code(code)
    if(teamCode != None):
        return True
    return False

def getTeamCode(mysql:MySQL, tid:int) -> TeamCode:
    """
    retrieves the team code from database
    :param tid: company teamcode is from
    :param mysql: database used
    :return: the TeamCode Object wanted
    """
    code = None
    dao_teamCode = DAOTeamCode(mysql)
    dao_teamCode.remove_teamcodes()
    code = dao_teamCode.get_teamcode_by_tid(tid)
    return code

def removeTeamCode(mysql:MySQL, tid:int) -> str:
    """
    removes teamCode attributed by tid
    :param tid: company code is for
    :param mysql: database used
    """
    dao_teamCode = DAOTeamCode(mysql)
    dao_teamCode.remove_teamCode_by_tid(tid)
    return "Team Code Disabled"

def generateTeamCode(mysql:MySQL, tid:int) -> str:
    """
    Creates a teamcode for the company
    :param tid: company code is for
    :param mysql: database used
    """
    dao_teamCode = DAOTeamCode(mysql)
    if(codeActive(mysql, tid)):
        removeTeamCode(mysql, tid)
    code = None
    while(code == None or checkCode(mysql,code)):
        # create an 8 char code
        code = ''.join(random.choice(string.ascii_uppercase +
                                    string.ascii_lowercase +
                                    string.digits) for _ in range(8))
    teamCode = TeamCode(tid,code)
    dao_teamCode.add_teamcode(teamCode)
    return "Successfully generated Team Code"

def get_tid_by_code(mysql:MySQL, code:str) -> int:
    """
    gets the tid by the code provided
    :param code: code to search for
    :param mysql: database in which code is found
    :return: tid of company joining or -1 if DNE
    """
    dao_teamCode = DAOTeamCode(mysql)
    tid = -1
    if(checkCode(mysql,code)):
        teamCode = dao_teamCode.get_teamCode_by_code(code)
        tid = teamCode.tid()
    return tid
