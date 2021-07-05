from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from classes.Role import Role


def remove_from_team(mysql, tid, uid, rid):
    dao_team = DAOTeam(mysql)
    if(int(rid) != Role.TEAM_OWNER.value):
        dao_team.remove_from_team(tid, uid)


def promote_admin(mysql, tid, uid, rid):
    # newRole should be id of admin
    dao_team = DAOTeam(mysql)
    team_to_update = dao_team.get_team_by_tid_uid(tid, uid)
    if(int(rid) != Role.TEAM_OWNER.value):
        team_to_update.rid = Role.TEAM_ADMIN.value
        dao_team.update_team(team_to_update)


def get_members(mysql, tid):
    dao_team = DAOTeam(mysql)
    dao_role = DAORole(mysql)
    users = dao_team.get_users_from_team(tid)
    if users:  # there are values in the database
        user_details = []
        for user in users:
            role = dao_role.get_role_by_rid(user.rid)
            user_details.append([user.name, role.name, user.contact,
                                user.uid, tid, user.rid])
        return user_details
