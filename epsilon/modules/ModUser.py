from classes.Role import Role
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from databaseAccess.DAOUser import DAOUser


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
    user_role = Role(user.rid)
    user_details = [user.name, user.description, user.contact, user_role.name]
    return user_details
