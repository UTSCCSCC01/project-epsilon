from typing import List
from flask_mysqldb import MySQL

from databaseAccess.DAOService import DAOService
from databaseAccess.DAOServiceType import DAOServiceType


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
