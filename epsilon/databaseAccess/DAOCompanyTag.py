from typing import List
from .DAO import DAO
from classes.CompanyTag import CompanyTag


class DAOCompanyTag(DAO):
    # child class of DAO.
    # contains database access methods related to company tag.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_company_tag_table(self) -> None:
        """
        Creates the Company Tags table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''create table IF NOT EXISTS CompanyTags(
                        ctid int auto_increment,
                        tid int null,
                        tag_id int null,
                        constraint CompanyTags_pk
                        primary key (ctid));''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Tags and Company tables to be created.
        """
        super().add_foreign_key("CompanyTags", "tag_id", "Tags")
        super().add_foreign_key("CompanyTags", "tid", "Company")

    def add_company_tag(self, company_tag: CompanyTag) -> None:
        """
        Add a new company tag into the database.
        :param company_tag: A CompnayTag object representing the
                            new company tag to insert.
        """
        self.modify_data(
            '''INSERT INTO CompanyTags (tid, tag_id) VALUES (%s, %s)''',
            (company_tag.tid, company_tag.tag_id))

    def get_search_data(self, keywords: List[str]) -> List[tuple]:
        """
        Returns Raw search data. Multiple copies of companies will be included.
        :param keywords: a list of keywords
        :return: A list of Raw search data.
        """
        # keywords_string = "{0}".format(keywords)
        # keywords_string = (keywords_string.replace("[", "("))
        # keywords_string = (keywords_string.replace("]", ")"))
        search_data = []
        for items in keywords:
            search_q = '''SELECT Company.name, Company.description
                    FROM CompanyTags, Tags, Company
                    WHERE Company.tid = CompanyTags.tid and
                    CompanyTags.tag_id = Tags.tag_id and
                    Tags.name LIKE '%''' + items + "%'"
            data = self.get_data(search_q, None)
            for company in data:
                search_data.append(company)
        print(search_data)
        return search_data
