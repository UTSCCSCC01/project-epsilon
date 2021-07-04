from typing import List
from .DAO import DAO
from classes.Role import Role


class DAORole(DAO):
    # child class of DAO.
    # contains database access methods related to role.

    def __init__(self, db):
        super().__init__(db)

    def create_role_table(self) -> None:
        """
        Creates the roles table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS Roles ("
                        "rid INTEGER,"
                        "role_type text not null,"
                        "PRIMARY KEY(rid)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_roles(self) -> None:
        """
        Populate roles with enum.
        """
        for r in Role:
            self.add_role(r)

    def add_role(self, role: Role) -> None:
        """
        Adds a new role into the database.
        :param role: A Role object representing the role to be added.
        """
        self.modify_data(
            '''INSERT INTO Roles (rid, role_type) VALUES (%s, %s)''',
            (role.value, role.name)
        )

    def get_roles(self) -> List[Role]:
        """
        Gets all roles in the database.
        :return: List of Role objects.
        """
        roles = []
        data = self.get_data('''SELECT * FROM Roles''', None)
        for role in data:
            roles.append(Role(role[0]))
        return roles

    def get_role_by_rid(self, rid) -> Role:
        """
        Gets a role from the database.
        :param rid: Role id of the role to be retrieved.
        :return: Role object representing the rid. None if not found.
        """
        role = None
        data = self.get_data('''SELECT * FROM Roles WHERE rid = %s''', (rid,))
        if data is not None:
            role = data[0]
        return Role(role[0])
