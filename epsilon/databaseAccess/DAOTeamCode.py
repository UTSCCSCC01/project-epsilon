from typing import List
from .DAO import DAO
from classes.TeamCode import TeamCode

class DAOTeamCode(DAO):
    # child class of DAO
    # contains database access methods related to team codes

    def __init__(self, db):
        super().__init__(db)
    
    def create_teamCode_table(self) -> None:
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS TeamCode (
                            tid int,
                            code text not null,
                            create_time timestamp default
                            current_timestamp null,
                            constraint TeamCode_pk
                            primary key (tid));''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass
    
    def add_foreign_key(self) -> None:
        super().add_foreign_key("TeamCode", "tid", "Company")
    
    def add_teamcode(self, teamCode: TeamCode) -> None:
        """
        Inserts a new code into the database
        :param teamCode: teamcode object representing what is inserted 
        """
        self.modify_data(
            '''INSERT INTO TeamCode (tid, code, create_time) 
            VALUES (%s, %s, CURRENT_TIMESTAMP);''',
            (teamCode.tid, teamCode.code))
    
    def update_teamcode(self, teamCode: TeamCode) -> None:
        """
        Updates entries of TeamCode in database
        :param teamCode: teamcode object representing object to be updated
        """
        self.modify_data(
            '''UPDATE TeamCode Set code = %s WHERE tid = %s''',
            (teamCode.code, teamCode.tid)
        )
    
    def get_teamcode_by_tid(self, tid: int) -> TeamCode:
        """
        Gets a code from the company
        :param tid: team id of teamcode retrieved
        :return: teamcode obj with tid given
                 None if dne
        """
        teamCode = None
        data = self.get_data("SELECT * FROM TeamCode WHERE tid = %s", (tid,))
        if data:
            teamCode = data[0]
            teamCode = TeamCode(teamCode[0],
                                teamCode[1],
                                teamCode[2])
        return teamCode

    def get_teamCode_by_code(self, code:str) -> TeamCode:
        """
        Gets a teamcode by code
        :param code: trial teamcode 
        :return: teamcode obj with code given
                 None if dne
        """
        teamCode = None
        data = self.get_data('''SELECT * FROM TeamCode
                                WHERE code = %s''', (code,))
        if data:
            teamCode = data[0]
            teamCode = TeamCode(teamCode[0],
                                teamCode[1],
                                teamCode[2])
        return teamCode            
    
    def remove_teamcodes(self) -> None:
        """
        Removes all teamCodes that are past 24 hrs old
        """
        self.modify_data(
            '''DELETE FROM TeamCode WHERE
               TIMESTAMPDIFF(HOUR,create_time,
               CURRENT_TIMESTAMP) > 24''',()
        )

    def remove_teamCode_by_tid(self, tid:int) -> None:
        """
        Removes singular teamCode referenced by tid
        :param tid: tid of company
        """
        self.modify_data(
            '''DELETE FROM TeamCode WHERE
               tid = %s''',(tid)
        )

