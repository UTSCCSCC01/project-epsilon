from typing import List

from classes.ServiceType import ServiceType
from classes.Service import Service
from databaseAccess.DAO import DAO


class DAOService(DAO):
    # child class of DAO.
    # contains database access methods related to service.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_services_table(self) -> None:
        """
        Creates the Services table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS Services (
            ser_id INTEGER auto_increment,
            uid INTEGER,
            ser_type_id INTEGER,
            title text not null,
            description text not null,
            price INTEGER not null,
            link text not null,
            constraint Services_pk
            primary key (ser_id))''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_keys(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Users and ServiceTypes tables to be created.
        """
        super().add_foreign_key("Services", "uid", "Users")
        super().add_foreign_key("Services", "ser_type_id", "ServiceTypes")

    def add_dummy_services(self) -> None:
        """
        Populate Services table with dummy data.
        """
        service1 = Service(ser_id=1, uid=6, ser_type_id=1, title="Design Thinking Workshop",
                           description="Join us for an online 4h workshop to learn design thinking!",
                           price=10, link="https://www.interaction-design.org/literature/topics/design-thinking")
        service2 = Service(ser_id=2, uid=6, ser_type_id=3, title="Lawyer",
                           description="If you need a lawyer, call us!",
                           price=23, link="https://www.thelawyer.com/")

        services_to_add = [service1, service2]

        for service in services_to_add:
            self.add_service(service)

    def add_service(self, service: Service) -> None:
        """
        Adds a new user into the database.
        :param service: A Service object representing the service to be added.
        """
        self.modify_data(
            '''INSERT INTO Services (uid, ser_type_id, title, description, price, link)
               VALUES (%s, %s, %s, %s, %s, %s)''',
            (service.uid, service.ser_type_id, service.title, service.description, service.price, service.link))

    def update_service(self, service: Service) -> None:
        """
        Updates the data of a service in the database.
        :param service: A Service object representing the service to be added.
        """
        self.modify_data(
            '''UPDATE Services Set ser_type_id = %s, title = %s, description = %s, price = %s, link = %s WHERE ser_id = %s''',
            (service.ser_type_id, service.title, service.description, service.price, service.link, service.ser_id))

    def get_services(self) -> List[Service]:
        """
        Gets all services in the database.
        :return: List of Service objects.
        """
        services = []
        data = self.get_data('''SELECT * FROM Services''', None)
        for service in data:
            services.append(Service(service[0], service[1], service[2],
                                    service[3], service[4], service[5], service[6]))
        return services

    def get_services(self, uid:int) -> List[Service]:        
        """
        Gets all services for given uid.
        :param uid: user id
        :return: List of Service objects.
        """
        services = []
        data = self.get_data('''SELECT * FROM Services WHERE uid = %s''', (uid,))
        for service in data:
            services.append(Service(service[0], service[1], service[2],
                                    service[3], service[4], service[5], service[6]))
        return services

    def remove_service(self, sid:int) -> None:
        """
        removes selected service
        :param sid: service id
        """
        self.modify_data('''DELETE FROM Services WHERE ser_id = %s''',(sid,))