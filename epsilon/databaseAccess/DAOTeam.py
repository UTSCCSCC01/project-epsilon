from typing import List
from .DAO import DAO
from classes.Team import Team
from classes.Role import Role
from classes.User import User


class DAOTeam(DAO):
    # child class of DAO.
    # contains database access methods related to team.
    # note, remember to update attributes that is returned
    # after updating schema.

    def __init__(self, db):
        super().__init__(db)

    def create_team_table(self) -> None:
        """
        Creates the Teams table.
        """
        cur = self.db.connection.cursor()
        try:
            cur.execute('''CREATE TABLE IF NOT EXISTS Teams (
                           tid INTEGER,
                           uid INTEGER,
                           rid INTEGER,
                           CONSTRAINT PK_Teams
                           PRIMARY KEY(tid, uid))''')
            self.db.connection.commit()
            cur.close()
        except BaseException as be:
            print(be)
            pass

    def add_foreign_key(self) -> None:
        """
        Add foreign key constraints to the created table.
        Require: Company, Users and Roles tables to be created.
        """
        super().add_foreign_key("Team", "tid", "Company")
        super().add_foreign_key("Team", "uid", "Users")
        super().add_foreign_key("Team", "rid", "Roles")

    def add_dummy_team_members(self) -> None:
        """
        Populate Team table with dummy data.
        Require: Company and User to already create dummy objects,
                 Roles to already be populated.
        """
        team_1 = Team(tid=1, uid=1, rid=Role.TEAM_ADMIN.value)
        team_2 = Team(tid=2, uid=2, rid=Role.TEAM_OWNER.value)
        teams_to_add = [team_1, team_2]

        for team in teams_to_add:
            self.add_team(team)

    def add_team(self, team: Team) -> None:
        """
        Adds a new team into the database.
        :param team: A Team object representing the team to be added.
        """
        self.modify_data(
            '''INSERT INTO Teams (tid, uid, rid) VALUES (%s, %s, %s)''',
            (team.tid, team.uid, team.rid)
        )

    def update_team(self, team: Team) -> None:
        """
        Updates the team in the database to team.
        :param team: A Team object representing the team to be updated.
        """
        self.modify_data(
            '''UPDATE Teams SET rid=%s WHERE uid=%s AND tid=%s ''',
            (team.rid, team.uid, team.tid))

    def get_teams(self) -> List[Team]:
        """
        Gets all teams in the database.
        :return: List of Team objects.
        """
        teams = []
        data = self.get_data('''SELECT * FROM Teams''', None)
        for team in data:
            teams.append(Team(team[0], team[1], team[2]))
        return teams

    def get_team_by_tid_uid(self, tid: int, uid: int) -> Team:
        """
        Gets a team from the database.
        :param tid: Team id of the team to be retrieved.
        :return: Team object representing the matching team. None if not found.
        """
        team = None
        data = self.get_data('''SELECT * FROM Teams
                                WHERE tid = %s AND uid = %s''', (tid, uid))
        if data is not None:
            team = data[0]
            team = Team(team[0], team[1], team[2])
        return team

    def get_users_from_team(self, tid: int) -> List[User]:
        """
        Gets all users in a team.
        :param tid: Team id of the users to be retrieved.
        :return: list of users objects representing the matching team.
        """
        users = []
        data = self.get_data(
            '''SELECT users.uid, teams.rid, users.name,
               users.contact, users.password, users.description
               FROM epsilon_db.users JOIN epsilon_db.teams
               ON users.uid = teams.uid
               WHERE tid = %s''', (tid,))

        for user in data:
            users.append(User(uid=user[0], rid=user[1], name=user[2],
                              contact=user[3], password=user[4],
                              description=user[5]))
        return users

    def remove_from_team(self, tid: int, uid: int) -> None:
        """
        Removes an employee from a team in the database.
        :param tid: team id of the employee to be removed.
        :param uid: user id of the employee to be removed.
        """
        self.modify_data(
            '''DELETE FROM Teams WHERE tid = %s AND uid = %s  ''', (tid, uid))

    def get_teams_by_uid(self, uid: int) -> List[Team]:
        """
        Gets all teams that user with uid is in.
        :return: List of Team objects.
        """
        teams = []
        data = self.get_data('''SELECT * FROM Teams
                                WHERE uid = %s''', (uid,))
        for team in data:
            teams.append(Team(team[0], team[1], team[2]))
        return teams

    def get_tids_by_admin_uid(self, uid: int) -> List[int]:
        """
        Gets all tid of companies that user is an admin.
        :return: List of tid
        """
        res = []
        data = self.get_data('''SELECT tid FROM Teams
                                WHERE uid = %s AND rid IN (%s, %s)''',
                             (uid, Role.TEAM_ADMIN.value,Role.TEAM_OWNER.value,))
        if data:
            for team in data:
                res.append(team[0])
        return res


    def get_all_company_id_with_job_posting(self) -> List[int]:
        """
        :return: List of tids with job postings.
        """
        res = []
        data = self.get_data_no_arg('''SELECT DISTINCT tid FROM JobPosting''')
        if data:
            for team in data:
                res.append(team[0])
        return res


    def get_tid_by_uid(self, uid: int) -> int:

        data = self.get_data('''SELECT tid FROM Teams
                                WHERE uid = %s''',
                             (uid,))
        if data:
            for team in data:
                return (team[0])
        return -1