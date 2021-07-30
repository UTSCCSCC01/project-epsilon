from typing import List


class DAO:

    def __init__(self, db):
        self.db = db

    def add_foreign_key(self, t_name: str, f_key: str,
                        ref_t_name: str) -> None:
        """
        Add a foreign key constraint  f_key to t_name referencing ref_t_name.
        :param t_name: the name of the table.
        :param f_key: foreign key of t_name.
        :param ref_t_name: the name of table to be reference.
        """
        try:
            cur = self.db.connection.cursor()
            cur.execute("ALTER TABLE " + t_name
                        + " ADD FOREIGN KEY(" + f_key + ") REFERENCES "
                        + ref_t_name + "(" + f_key + ")",
                        None)
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def modify_data(self, sql_q: str, data: tuple) -> None:
        """
        Make changes to database with sql_q.
        :param sql_q: the sql query string
        :param data: a tuple containing strings to include in query.
        """
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q, data)
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def get_data(self, sql_q: str, data: tuple) -> List[tuple]:
        """
        Get a list of data with sql_q.
        :param sql_q: the sql query string
        :param data: a tuple containing srings to include in query.
        """
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q, data)
            data = cur.fetchall()
            cur.close()
            return data
        except BaseException as be:
            print(be)
            pass

    def delete_all(self) -> None:
        """
        Delete all tables in the database.
        """
        t_names = ["JobApplication", "JobPosting", "TeamCode",
                   "Teams", "Request", "Services", "Users", "Roles",
                   "CompanyTags", "Company", "RStatus",
                   "Tags", "Industry", "Type", "ServiceTypes"]
        for t_name in t_names:
            self.drop_table(t_name)

    def drop_table(self, t_name: str) -> None:
        """
        Drop a table with name t_name.
        :param t_name: the name of the table.
        """
        try:
            cur = self.db.connection.cursor()
            cur.execute('''DROP TABLE IF EXISTS ''' + t_name, None)
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass


    def get_data_no_arg(self, sql_q: str) -> List[tuple]:
        """
        Get a list of data with sql_q.
        :param sql_q: the sql query string
        :param data: a tuple containing strings to include in query.
        """
        try:
            cur = self.db.connection.cursor()
            cur.execute(sql_q)
            data = cur.fetchall()
            cur.close()
            return data
        except BaseException as be:
            print(be)
            pass