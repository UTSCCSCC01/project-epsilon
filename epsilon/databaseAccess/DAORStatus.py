from typing import List
from .DAO import DAO
from classes.RStatus import RStatus


class DAORStatus(DAO):
    # child class of DAO.
    # contains database access methods related to rStatus,
    # request status.

    def __init__(self, db):
        super().__init__(db)

    def create_rstatus_table(self) -> None:
        """
        Creates the rStatus table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute("CREATE TABLE IF NOT EXISTS RStatus ("
                        "sid INTEGER,"
                        "name text not null,"
                        "PRIMARY KEY(sid)"
                        ")")
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_r_statuses(self) -> None:
        """
        Populate rStatus with enum.
        """
        for r in RStatus:
            self.add_r_status(r)

    def add_r_status(self, r_status: RStatus) -> None:
        """
        Adds a new r_status into the database.
        :param r_status: A RStatus object representing
                         the r_status to be added.
        """
        self.modify_data(
            '''INSERT INTO RStatus (sid, name) VALUES (%s, %s)''',
            (r_status.value, r_status.name)
        )
