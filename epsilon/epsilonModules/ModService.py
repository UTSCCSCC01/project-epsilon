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
    :return List of service details of all the services.
            List of lists with the form [ser_id, uid, ser_type_id, title, description, price, link].
    """
    dao_service = DAOService(mysql)
    dao_service_type = DAOServiceType(mysql)
    services = dao_service.get_services()

    service_details = []
    for service in services:
        ser_type = dao_service_type.get_ser_type_by_id(service.ser_type_id)
        ser_type_name = ser_type.name.replace("_", " ").title()
        service_details.append([service.ser_id, service.uid, ser_type_name, service.title, service.description,
                                service.price, service.link])
    return service_details


def add_service(mysql: MySQL, uid: int, title: str, description: str, price: int,
                link: str, service_type: int) -> str:
    """
    Registers a User into the database
    :param mysql: mysql db.
    :param uid: uid of the user posting the service
    :param title: title of new service.
    :param description: description of new service.
    :param price: price of new service.
    :param link: the link of new service.
    :param service_type: the service_type id for new service.
    :return: status message of adding user.
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