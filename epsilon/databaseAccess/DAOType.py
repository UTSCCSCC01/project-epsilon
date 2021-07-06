from typing import List
from .DAO import DAO
from classes.Type import Type


class DAOType(DAO):
    # child class of DAO.
    # contains database access methods related to type.

    def __init__(self, db):
        super().__init__(db)

    def create_type_table(self) -> None:
        """
        Creates the type table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS Type ("
                        "type_id INTEGER,"
                        "user_type text not null,"
                        "PRIMARY KEY(type_id)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_types(self) -> None:
        """
        Populate types with enum.
        """
        for t in Type:
            self.add_type(t)

    def add_type(self, type: Type) -> None:
        """
        Adds a new type into the database.
        :param type: A Type object representing the type to be added.
        """
        self.modify_data(
            '''INSERT INTO Type (type_id, user_type) VALUES (%s, %s)''',
            (type.value, type.name)
        )

    def get_types(self) -> List[Type]:
        """
        Gets all types in the database.
        :return: List of Type objects.
        """
        types = []
        data = self.get_data('''SELECT * FROM Type''', None)
        for type in data:
            types.append(Type(type[0]))
        return types

    def get_type_by_type_id(self, type_id) -> Type:
        """
        Gets a type from the database.
        :param type_id: Type id of the user type to be retrieved.
        :return: Type object representing the type id. None if not found.
        """
        type = None
        data = self.get_data('''SELECT * FROM Type WHERE type_id = %s''',
                             (type_id,))
        if data is not None:
            type = data[0]
        return Type(type[0])
