from typing import List
from flask_mysqldb import MySQL

from classes.Service import Service
from databaseAccess.DAOService import DAOService
from databaseAccess.DAOServiceType import DAOServiceType
from exceptions.FormIncompleteError import FormIncompleteError


def get_services(mysql: MySQL) -> List:
    """
    Return all the services that have been posted.
    :param mysql: mysql db.
    :return List of services.
    """
    dao_service = DAOService(mysql)
    services = dao_service.get_services()

    return services


def add_service(mysql: MySQL, uid: int, title: str, description: str, price: int,
                link: str, service_type: int) -> str:
    """
    Registers a Service into the database
    :param mysql: mysql db.
    :param uid: uid of the user posting the service
    :param title: title of new service.
    :param description: description of new service.
    :param price: price of new service.
    :param link: the link of new service.
    :param service_type: the service_type id for new service.
    :return: status message of adding service.
    """
    dao_service = DAOService(mysql)
    # check if any required fields isn't filled
    if uid < 0 or len(title) == 0 or len(description) == 0 or price == "0" or len(link) == 0 or service_type is None:
        raise FormIncompleteError()
    else:
        try:
            # create new service
            service = Service(uid=uid, title=title, description=description, price=price, link=link, ser_type_id=service_type)
            dao_service.add_service(service)
            # send success prompt
            message = "Service successfully created!"
            return message
        except Exception as e:
            # display issue w db
            raise e
