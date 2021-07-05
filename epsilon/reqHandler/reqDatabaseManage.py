from databaseAccess.DAOUser import DAOUser
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOTag import DAOTag
from databaseAccess.DAORStatus import DAORStatus
from databaseAccess.DAORole import DAORole
from databaseAccess.DAORequest import DAORequest
from databaseAccess.DAOIndustry import DAOIndustry
from databaseAccess.DAOCompanyTag import DAOCompanyTag
from databaseAccess.DAOCompany import DAOCompany
from modules.registration import add_dummy_companies
from databaseAccess.DAO import DAO
from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL


def delete_tables(mysql):
    dao = DAO(mysql)
    dao.delete_all()
    return "all tables are deleted!"


def create_tables(mysql):
    dao_company = DAOCompany(mysql)
    dao_company_tag = DAOCompanyTag(mysql)
    dao_industry = DAOIndustry(mysql)
    dao_request = DAORequest(mysql)
    dao_role = DAORole(mysql)
    dao_rstatus = DAORStatus(mysql)
    dao_tag = DAOTag(mysql)
    dao_team = DAOTeam(mysql)
    dao_user = DAOUser(mysql)

    dao_company.create_company_table()
    dao_company_tag.create_company_tag_table()
    dao_industry.create_industry_table()
    dao_request.create_request_table()
    dao_role.create_role_table()
    dao_rstatus.create_rstatus_table()
    dao_tag.create_tag_table()
    dao_team.create_team_table()
    dao_user.create_user_table()

    dao_company.add_foreign_key()
    dao_company_tag.add_foreign_key()
    dao_request.add_foreign_key()
    dao_tag.add_foreign_key()
    dao_team.add_foreign_key()
    dao_user.add_foreign_key()

    dao_role.add_roles()
    dao_rstatus.add_r_statuses()
    dao_industry.add_dummy_industries()
    # to prevent circular import, dummy companies are added by registration
    add_dummy_companies(mysql)
    dao_user.add_dummy_users()
    dao_team.add_dummy_team_members()
    dao_request.add_dummy_requests()

    users = dao_user.get_users()
    teams = dao_team.get_teams()
    roles = dao_role.get_roles()
    companies = dao_company.get_companies()

    t_names = ["Teams", "Request", "Users", "Roles",
               "CompanyTags", "Company", "RStatus",
               "Tags", "Industry"]

    output = "The following tables are populated! </br> <ul>"
    for t_name in t_names:
        output += "<li>" + t_name + "</li>"

    output += "</ul> </br>Also five dummy employees:</br>"
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
        output += str(company.name) + ":"+str(company.description) + "</br>"

    return output