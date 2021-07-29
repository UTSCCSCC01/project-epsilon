from classes.Type import Type
from typing import List
from .DAO import DAO
from classes.User import User


class DAOUser(DAO):
    # child class of DAO.
    # contains database access methods related to user.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_user_table(self) -> None:
        """
        Creates the Users table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS Users (
            uid INTEGER auto_increment,
            type_id INTEGER,
            name text not null,
            contact text not null,
            password text not null,
            description text not null,
            constraint Users_pk
            primary key (uid))''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Roles tables to be created.
        """
        super().add_foreign_key("Users", "type_id", "Types")

    def add_dummy_users(self) -> None:
        """
        Populate Users table with dummy data.
        """
        user1 = User(uid=1, type_id=Type.STARTUP_USER.value,
                     name="Paula", contact="ok@gmail.com",
                     description="Hi, I am Paula, team owner of Epsilon.",
                     password="admin")
        user2 = User(uid=2, type_id=Type.STARTUP_USER.value,
                     name="Tim", contact="ko@gmail.com",
                     description="This is Tim, owner of Company Delta.",
                     password="admin")
        user3 = User(uid=3, type_id=Type.STARTUP_USER.value,
                     name="Pritish", contact="lp@gmail.com",
                     description="I am waiting to join team Epsilon!.",
                     password="admin")
        user4 = User(uid=4, type_id=Type.STARTUP_USER.value,
                     name="Sam", contact="opll@gmail.com",
                     description="Here comes Sam.",
                     password="admin")
        user5 = User(uid=5, type_id=Type.STARTUP_USER.value,
                     name="Water", contact="no@gmail.com",
                     description="Water is good.",
                     password="admin")
        user6 = User(uid=6, type_id=Type.SERVICE_PROVIDER.value,
                     name="Rodrigo", contact="yes@gmail.com",
                     description="Water is great.",
                     password="admin")

        users_to_add = [user1, user2, user3, user4, user5, user6]

        for user in users_to_add:
            self.add_user(user)

    def add_user(self, user: User) -> None:
        """
        Adds a new user into the database.
        :param user: A User object representing the user to be added.
        """
        self.modify_data(
            '''INSERT INTO Users (type_id, name, contact, password,description)
               VALUES (%s, %s, %s, %s, %s)''',
            (user.type_id, user.name, user.contact,
             user.password, user.description))

    def update_user(self, user: User) -> None:
        """
        Updates the data of a user in the database.
        :param user: A User object representing the user to be modified.
        """
        self.modify_data(
            '''UPDATE Users Set name = %s, description = %s WHERE uid = %s''',
            (user.name, user.description, user.uid))

    def get_users(self) -> List[User]:
        """
        Gets all users in the database.
        :return: List of User objects.
        """
        users = []
        data = self.get_data('''SELECT * FROM Users''', None)
        for user in data:
            users.append(User(user[0], user[1], user[2],
                              user[3], user[4], user[5]))
        return users

    def get_user_by_uid(self, uid: int) -> User:
        """
        Gets one user with uid matching the parameter.
        :param: uid (int) is the user ID of the user you want to get.
        :return: User object or None if not found.
        """
        user = None
        data = self.get_data('''SELECT * FROM Users WHERE uid = %s''', (uid,))
        if data:
            user = data[0]
            user = User(user[0], user[1], user[2],
                        user[3], user[4], user[5])
        return user

    def get_user_by_contact(self, email: str) -> User:
        """
        Gets a user from the database.
        :param email: Email of the user to be retrieved.
        :return: User object representing the matching User. None if not found.
        """
        user = None
        data = self.get_data('''SELECT * FROM Users WHERE contact = %s''',
                             (email,))
        if data:
            user = data[0]
            user = User(user[0], user[1], user[2],
                        user[3], user[4], user[5])

        # to be added get rid from teams table
        return user
