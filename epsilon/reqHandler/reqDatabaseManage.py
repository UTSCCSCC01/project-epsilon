from databaseAccess.DAOJobPosting import DAOJobPosting
from databaseAccess.DAOJobApplication import DAOJobApplication
from databaseAccess.DAOType import DAOType
from databaseAccess.DAOUser import DAOUser
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOTag import DAOTag
from databaseAccess.DAORStatus import DAORStatus
from databaseAccess.DAORole import DAORole
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAOIndustry import DAOIndustry
from databaseAccess.DAOCompanyTag import DAOCompanyTag
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOTeamCode import DAOTeamCode
from databaseAccess.DAOService import DAOService
from databaseAccess.DAOServiceType import DAOServiceType
from databaseAccess.DAO import DAO
from epsilonModules.ModCompany import add_dummy_companies
from flask_mysqldb import MySQL


def delete_tables(mysql: MySQL) -> str:
    """
    Deletes all tables from the database.
    :param mysql: mysql db.
    """
    dao = DAO(mysql)
    dao.delete_all()
    return "all tables are deleted!"


def create_tables(mysql: MySQL) -> str:
    """
    Create tables in database.
    :param mysql: mysql db.
    """
    # DAO objects
    dao_company = DAOCompany(mysql)
    dao_company_tag = DAOCompanyTag(mysql)
    dao_industry = DAOIndustry(mysql)
    dao_request = DAORequest(mysql)
    dao_role = DAORole(mysql)
    dao_rstatus = DAORStatus(mysql)
    dao_tag = DAOTag(mysql)
    dao_team = DAOTeam(mysql)
    dao_user = DAOUser(mysql)
    dao_type = DAOType(mysql)
    dao_job_application = DAOJobApplication(mysql)
    dao_job_posting = DAOJobPosting(mysql)
    dao_teamCode = DAOTeamCode(mysql)
    dao_service = DAOService(mysql)
    dao_service_type = DAOServiceType(mysql)

    # table creation
    dao_company.create_company_table()
    dao_company_tag.create_company_tag_table()
    dao_industry.create_industry_table()
    dao_request.create_request_table()
    dao_role.create_role_table()
    dao_rstatus.create_rstatus_table()
    dao_tag.create_tag_table()
    dao_team.create_team_table()
    dao_user.create_user_table()
    dao_type.create_type_table()
    dao_job_application.create_job_application_table()
    dao_job_posting.create_job_posting_table()
    dao_teamCode.create_teamCode_table()
    dao_service.create_services_table()
    dao_service_type.create_service_types_table()

    # foreign keys
    dao_company.add_foreign_key()
    dao_company_tag.add_foreign_key()
    dao_tag.add_foreign_key()
    dao_team.add_foreign_key()
    dao_user.add_foreign_key()
    dao_job_application.add_foreign_key()
    dao_job_posting.add_foreign_key()
    dao_teamCode.add_foreign_key()
    dao_service.add_foreign_keys()

    # add that does not have foreign key constraint
    dao_role.add_roles()
    dao_type.add_types()
    dao_rstatus.add_r_statuses()
    dao_industry.add_dummy_industries()
    dao_service_type.add_service_types()

    # add that has foreign key constraint
    # to prevent circular import, dummy companies are added by registration
    add_dummy_companies(mysql)
    dao_user.add_dummy_users()
    dao_team.add_dummy_team_members()
    dao_request.add_dummy_requests()
    dao_job_posting.add_dummy_job_postings()
    dao_job_application.add_dummy_job_applications()
    dao_service.add_dummy_services()

    users = dao_user.get_users()
    teams = dao_team.get_teams()
    roles = dao_role.get_roles()
    companies = dao_company.get_companies()
    types = dao_type.get_types()
    job_postings = dao_job_posting.get_job_postings()
    job_applications = dao_job_application.get_job_postings()

    services = dao_service.get_services()
    service_types = dao_service_type.get_service_types()

    t_names = ["Teams", "Users", "Roles",
               "CompanyTags", "Company", "RStatus",
               "Tags", "Industry", "Type", "JobApplication", "JobPosting",
               "Services", "ServiceTypes", "TeamCode"]

    output = "The following tables are populated! </br> <ul>"
    for t_name in t_names:
        output += "<li>" + t_name + "</li>"

    output += "</ul> </br>Also six dummy employees:</br>"
    for user in users:
        output += str(user) + "</br>"
    output += "Also two dummy teams:</br>"
    for team in teams:
        output += str(team) + "</br>"
    output += "Also three roles:</br>"
    for role in roles:
        output += str(role.name) + "</br>"
    output += "Also two companies:</br>"
    for company in companies:
        output += str(company.name) + ":" + str(company.description) + "</br>"
    output += "Also three types:</br>"
    for type in types:
        output += str(type.name) + "</br>"
    output += "Also three job postings:</br>"
    for job_p in job_postings:
        output += str(job_p) + "</br>"
    output += "Also four job applications:</br>"
    for job_a in job_applications:
        output += str(job_a) + "</br>"
    output += "Also two services:</br>"
    for service in services:
        output += str(service.title) + "</br>"
    output += "Also five service types:</br>"
    for st in service_types:
        output += str(st.name) + "</br>"

    return output
