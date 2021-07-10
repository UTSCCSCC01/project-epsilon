from typing import List
from .DAO import DAO
from classes.Industry import Industry


class DAOIndustry(DAO):
    # child class of DAO.
    # contains database access methods related to Industry.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_industry_table(self) -> None:
        """
        Creates the Industry table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''create table IF NOT EXISTS Industry (
                        ind_id int auto_increment,
                        name text not null,
                        constraint Industry_pk
                        primary key (ind_id));''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_dummy_industries(self) -> None:
        """
        Populate Industry table with dummy data.
        """
        industry = Industry(name="Other")
        self.add_industry(industry)

    def add_industry(self, industry: Industry) -> None:
        """
        Adds the Industry to the industry table.
        """
        self.modify_data(
                '''INSERT INTO Industry (name) VALUES (%s)''',
                (industry.name,))

    def get_industries(self) -> List[Industry]:
        """
        Gets the list of all industries from the Industry table.
        :return: A list of Industry Objects.
        """
        industry = []
        data = self.get_data('''SELECT * FROM Industry''', None)
        for ind in data:
            industry.append(Industry(ind[0], ind[1]))
        return industry
