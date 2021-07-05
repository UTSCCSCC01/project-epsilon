from exceptions.ObjectNotExistsError import ObjectNotExistsError
from classes.Team import Team
from classes.RStatus import RStatus
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAORole import DAORole
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOCompany import DAOCompany
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
    if not users:
        raise ObjectNotExistsError("Your team")
    # there are values in the database
    user_details = []
    for user in users:
        role = dao_role.get_role_by_rid(user.rid)
        user_details.append([user.name, role.name, user.contact,
                            user.uid, tid, user.rid])
    return user_details


def get_join_requests(mysql, tid):
    dao_request = DAORequest(mysql)
    dao_company = DAOCompany(mysql)

    requests = dao_request.get_requests_by_tid_sid(tid, RStatus.PENDING.value)
    company = dao_company.get_company_by_tid(tid)
    if not company:
        raise ObjectNotExistsError("Your team")
    data = []
    for req in requests:
        data.append([req.uid, req.create_date, req.req_id])
    return data, company.name


def team_request_accept(mysql, req_id):
    # Update Request and Teams to reflect on accept action
    dao_request = DAORequest(mysql)
    dao_team = DAOTeam(mysql)
    message = team_request_update(dao_request, req_id, RStatus.ACCEPTED.value)

    if message is None:
        request = dao_request.get_request_by_req_id(req_id)
        team = Team(request.tid, request.uid, Role.TEAM_MEMBER.value)
        dao_team.add_team(team)
        message = "Accept Successful!"
    return message


def team_request_decline(mysql, req_id):
    # Update Request to reflect on decline action
    dao_request = DAORequest(mysql)
    message = team_request_update(dao_request, req_id, RStatus.REJECTED.value)
    if message is None:
        message = "Decline Successful!"
    return message


def team_request_update(dao_request, req_id, status):
    request = dao_request.get_request_by_req_id(req_id)
    if request.sid == RStatus.PENDING.value:
        request.sid = status
        dao_request.update_request(request)
        return
    else:
        return "Status is not pending!"
