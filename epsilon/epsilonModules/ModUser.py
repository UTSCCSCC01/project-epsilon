from typing import List

from classes.Type import Type
from classes.User import User
from databaseAccess.DAOUser import DAOUser
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from exceptions.InputInvalidError import InputInvalidError
from exceptions.FormIncompleteError import FormIncompleteError
from exceptions.ObjectExistsError import ObjectExistsError
from exceptions.LongNameError import LongNameError
from flask_mysqldb import MySQL
import re


def update_user(mysql: MySQL, uid: int, name: str,
                description: str, contact: str) -> str:
    """
    Updates a user with given parameters.
    :param mysql: mysql db.
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


def get_user_by_uid(mysql: MySQL, uid: int) -> User:
    """
    Return the detaisl of a user.
    :param mysql: mysql db.
    :param uid: uid of user.
    :return user.
    """
    dao_user = DAOUser(mysql)
    user = dao_user.get_user_by_uid(uid)
    if user is None:
        raise ObjectNotExistsError("The user")

    return user


# EP-23 User Registration
def user_registration(mysql: MySQL, name: str, email: str,
                      pwd: str, u_type: int) -> str:
    '''
    Registers a User into the database
    :param mysql: mysql db.
    :param name: name of new user.
    :param email: email of new user.
    :param pwd: password of new user.
    :param u_type: the type id for new user.
    :return: status message of adding user.
    '''
    dao_user = DAOUser(mysql)
    # check if any required fields isn't filled
    if (len(email) == 0 or len(pwd) == 0 or len(name) == 0 or u_type is None):
        raise FormIncompleteError()
    # ensure name is not more than 6 letters
    elif(len(name) >= 7):
        raise LongNameError()
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
            user = User(type_id=u_type,
                        name=name[0:6], contact=email, password=pwd)
            dao_user.add_user(user)
            # send success prompt
            message = "Account successfully created!"
            return message
        except Exception as e:
            # display issue w db
            raise e


def user_login(mysql: MySQL, username: str, password: str) -> User:
    """
    Checks if inputs are valid username and correct password.
    :param mysql: mysql db.
    :param username: email of user.
    :param password: password of user.
    :return: User object matching username.
    """
    if (len(username) == 0 or len(password) == 0):
        raise FormIncompleteError()
    dao_user = DAOUser(mysql)
    user = dao_user.get_user_by_contact(username)
    if (not user):
        raise ObjectNotExistsError("The email",
                                   " does not exist in our record.")
    elif user.password != password:
        raise InputInvalidError("Password does not match.")
    return user


def get_user_profile(mysql: MySQL, uid: int) -> List:
    """
    Return the detaisl of a user.
    :param mysql: mysql db.
    :param uid: uid of user.
    :return List of user details.
    """
    dao_user = DAOUser(mysql)
    user = dao_user.get_user_by_uid(uid)
    if user is None:
        raise ObjectNotExistsError("The user")
    user_type = Type(user.type_id)
    user_type_name = user_type.name.replace("_", " ").title()
    user_details = [user.name, user.description, user.contact, user_type_name]
    return user_details
