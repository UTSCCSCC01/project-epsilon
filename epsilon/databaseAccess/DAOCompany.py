from typing import List
from .DAO import DAO
from classes.Company import Company


class DAOCompany(DAO):
    # child class of DAO.
    # contains database access methods related to company.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_company_table(self) -> None:
        """
        Creates the Company table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS Company (
                           tid int auto_increment,
                           name text not null,
                           description text not null,
                           ind_id int,
                           create_date timestamp default
                           current_timestamp null,
                           constraint Company_pk
                           primary key (tid));''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Industry table to be created.
        """
        super().add_foreign_key("Company", "ind_id", "Industry")

    def add_company(self, company: Company) -> None:
        """
        Adds a new company into the database.
        :param company: A Company object representing the company to be added.
        """
        self.modify_data(
            '''INSERT INTO Company (name, description, ind_id)
               VALUES (%s, %s, %s)''',
            (company.name,
             company.description,
             company.ind_id))

    def update_company(self, company: Company) -> None:
        """
        Updates the data of a company in the database.
        :param company: A Company object representing the user to be modified.
        """
        self.modify_data(
            '''UPDATE Company Set name = %s, description = %s, ind_id = %s
               WHERE tid = %s''',
            (company.name, company.description, company.ind_id, company.tid))

    def get_companies(self) -> List[Company]:
        """
        Gets all companies in the database.
        :return: List of Company objects.
        """
        companies = []
        data = self.get_data('''SELECT * FROM Company''', None)
        for company in data:
            companies.append(
                Company(
                    company[0],
                    company[1],
                    company[2],
                    company[3]))
        return companies

    def get_company_by_tid(self, tid: int) -> Company:
        """
        Gets a company from the database.
        :param tid: Team id of the company to be retrieved.
        :return: compnay object representing the matching company.
                 None if not found.
        """
        company = None
        data = self.get_data('''SELECT * FROM Company
                                WHERE tid = %s''', (tid,))
        if data:
            company = data[0]
            company = Company(
                    company[0],
                    company[1],
                    company[2],
                    company[3])
        return company

    def get_company_by_name(self, name: str) -> Company:
        """
        Gets a company from the database.
        :param name: name of the company to be retrieved.
        :return: Company object representing the matching Company.
                 None if not found.
        """
        company = None
        data = self.get_data('''SELECT * FROM Company
                                WHERE name = %s''', (name,))
        if data:
            company = data[0]
            company = Company(
                    company[0],
                    company[1],
                    company[2],
                    company[3])
        return company
