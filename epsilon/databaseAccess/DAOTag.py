from .DAO import DAO
from classes.Tag import Tag


class DAOTag(DAO):
    # child class of DAO.
    # contains database access methods related to tag.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_tag_table(self) -> None:
        """
        Creates the Tags table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''create table IF NOT EXISTS Tags(
                           tag_id int auto_increment,
                           name text not null,
                           ind_id int,
                           constraint Tags_pk
                           primary key (tag_id));''')
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
        super().add_foreign_key("Tags", "ind_id", "Industry")

    def add_tag(self, tag: Tag) -> None:
        """
        Adds a new tag into the database.
        :param tag: A Tag object representing the tag to be added.
        """
        self.modify_data(
            '''INSERT INTO Tags (name, ind_id) VALUES (%s, %s)''',
            (tag.name, tag.ind_id))

    def get_tag_by_name(self, name: str) -> Tag:
        """
        Gets a team from the database.
        :param name: the name of the tag
        :return: Tag object representing the matching tag. None if not found.
        """
        tag = None
        data = self.get_data('''SELECT * FROM Tags WHERE name = %s''', (name,))
        if data is not None:
            tag = data[0]
            tag = Tag(tag_id=tag[0], name=tag[1], ind_id=tag[2])
        return tag
