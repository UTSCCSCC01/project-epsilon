from typing import List
from .DAO import DAO
from classes.ServiceType import ServiceType


class DAOServiceType(DAO):
    # child class of DAO.
    # contains database access methods related to role.

    def __init__(self, db):
        super().__init__(db)

    def create_service_types_table(self) -> None:
        """
        Creates the service types table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS ServiceTypes ("
                        "ser_type_id INTEGER,"
                        "service_type text not null,"
                        "PRIMARY KEY(ser_type_id)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_service_types(self) -> None:
        """
        Populate service types with enum.
        """
        for st in ServiceType:
            self.add_service_type(st)

    def add_service_type(self, service: ServiceType) -> None:
        """
        Adds a new role into the database.
        :param service: A ServiceType object representing the service type to be added.
        """
        self.modify_data(
            '''INSERT INTO ServiceTypes (ser_type_id, service_type) VALUES (%s, %s)''',
            (service.value, service.name)
        )

    def get_service_types(self) -> List[ServiceType]:
        """
        Gets all service types in the database.
        :return: List of ServiceType objects.
        """
        service_types = []
        data = self.get_data('''SELECT * FROM ServiceTypes''', None)
        for st in data:
            service_types.append(ServiceType(st[0]))
        return service_types

    def get_ser_type_by_id(self, ser_type_id: int) -> ServiceType:
        """
        Gets a service type from the database.
        :param ser_type_id: Ser type ID of the service type to be retrieved.
        :return: ServiceType object representing the ser_type_id. None if not found.
        """
        service_type = None
        data = self.get_data('''SELECT * FROM ServiceTypes WHERE ser_type_id = %s''', (ser_type_id,))
        if data is not None:
            service_type = data[0]
        return ServiceType(service_type[0])
