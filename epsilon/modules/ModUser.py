from classes.Type import Type
from classes.Role import Role
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from databaseAccess.DAOUser import DAOUser
from exceptions.InputInvalidError import InputInvalidError
from exceptions.FormIncompleteError import FormIncompleteError
from exceptions.ObjectExistsError import ObjectExistsError
from databaseAccess.DAOUser import DAOUser
from flask_mysqldb import MySQL
from classes.User import User
import re


def update_user(mysql, uid: int, name: str,
                description: str, contact: str) -> str:
    """
    Updates a user with given parameters.
    :param dao: DAO from app.
    :param uid: uid of user.
    :param name: name of user.
    :param description: description of user.
    :param contact: contact of user.
    :return: Message whether update was successful.
    """
    dao_user = DAOUser(mysql)
    user_to_update = dao_user.get_user_by_uid(uid)
    if user_to_update is None:
        raise ObjectNotExistsError("The user")
    else:
        user_to_update.name = name
        user_to_update.description = description
        user_to_update.contact = contact
        dao_user.update_user(user_to_update)
        return "User info updated."


def get_user_profile(mysql, uid):
    dao_user = DAOUser(mysql)
    user = dao_user.get_user_by_uid(uid)
    if user is None:
        raise ObjectNotExistsError("The user")
    user_type = Type(user.type_id)
    user_type_name = user_type.name.replace("_", " ").title()
    user_details = [user.name, user.description, user.contact, user_type_name]
    return user_details


# EP-23 User Registration
def user_registration(mysql: MySQL, name, email, pwd, u_type):
    '''
    Registers a User into the database
    :param mysql: database to access
    :return: rendered template of the user registration page
    '''
    dao_user = DAOUser(mysql)
    # check if any required fields isn't filled
    if (len(email) == 0 or len(pwd) == 0 or len(name) == 0 or u_type is None):
        raise FormIncompleteError()
    # check if the user email is already in use (username)
    elif (dao_user.get_user_by_contact(email) is not None):
        raise ObjectExistsError("Email", " already in use, "
                                + "please use another one.")
    # check email format
    elif (not re.search(".+@{1}.+\..+", email) or
          len(re.findall("@", email)) > 1):
        raise InputInvalidError("Email incorrect format")
    else:
        try:
            # create new user
            user = User(type_id=u_type, name=name, contact=email, password=pwd)
            dao_user.add_user(user)
            # send success prompt
            message = "Account successfully created!"
            return message
        except Exception as e:
            # display issue w db
            raise e
