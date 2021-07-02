import sys
sys.path.append('../epsilon/databaseAccess')
from DAO import DAO


def update_user(dao: DAO, uid: int, name: str,
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
    user_to_update = dao.get_user(uid)
    if user_to_update is None:
        return "Error: The user does not exist."
    else:
        user_to_update.name = name
        user_to_update.description = description
        user_to_update.contact = contact
        dao.update_user(user_to_update)
        return "User info updated."
