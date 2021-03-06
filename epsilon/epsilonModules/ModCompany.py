from datetime import datetime
from epsilonModules.ModTeam import add_team
from typing import List

from classes.Company import Company
from classes.CompanyTag import CompanyTag
from classes.Role import Role
from classes.Tag import Tag
from classes.Team import Team
from classes.Type import Type
from classes.User import User
from databaseAccess.DAOCompany import DAOCompany
from databaseAccess.DAOCompanyTag import DAOCompanyTag
from databaseAccess.DAOTag import DAOTag
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOUser import DAOUser
from exceptions.FormIncompleteError import FormIncompleteError
from exceptions.ObjectExistsError import ObjectExistsError
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from flask_mysqldb import MySQL
from rake_nltk import Rake


def check_team_exists(dao_company: DAOCompany, name: str) -> bool:
    """
    Check if the name for a new company exists in the database.
    :param dao_company: DAO object for Company class.
    :param name: name of new company.
    :return true if name matches (case insensitive), false otherwise.
    """
    # Returns 1 if match is found else returns 0
    companies = dao_company.get_companies()
    for company in companies:
        if company.name.lower() == name.lower():
            return True
    return False


def is_pos_int(s) -> bool:
    """
    Checks if the char is a integer or not
    :param s: The character
    :return Bool based on if the char is int or not.
    """
    # EP-1: Team management
    try:
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def update_tags_from_team_desc(dao_company: DAOCompany, dao_tag: DAOTag,
                               dao_company_tag: DAOCompanyTag,
                               desc: str, team_name: str) -> None:
    """
    Adds tags to the database and links them to the team
    :param dao_company: The DAO object for Company class
    :param dao_tag: The DAO object for tag class
    :param dao_company_tag: The DAO object for CompanyTag class
    :param desc: The team description
    :param team_name: the name of the team
    """
    rake_nltk_var = Rake()
    rake_nltk_var.extract_keywords_from_text(desc)
    keyword_extracted = rake_nltk_var.get_ranked_phrases()
    keyword_extracted.append(team_name)

    companies = dao_company.get_companies()
    tid = 0
    for team in companies:
        if team.name == team_name:
            tid = team.tid
            break
    for keywords in keyword_extracted:
        tags = Tag(name=keywords)
        dao_tag.add_tag(tags)
        tag = dao_tag.get_tag_by_name(keywords)
        company_tags = CompanyTag(tag_id=tag.tag_id, tid=tid)
        dao_company_tag.add_company_tag(company_tags)


def register_team(mysql: MySQL, name: str, desc: str, indust: int, uid: int) -> str:
    """
    Renders the template for team registration.
    :param mysql: mysql db.
    :param name: name for new company.
    :param desc: team description for new company.
    :param indust: ind_id for new company.
    :return response message for the registration.
    """
    dao_company = DAOCompany(mysql)
    dao_user = DAOUser(mysql)
    dao_team = DAOTeam(mysql)
    dao_tag = DAOTag(mysql)
    dao_company_tag = DAOCompanyTag(mysql)

    if len(name) == 0 or len(desc) == 0 or len(indust) == 0:
        raise FormIncompleteError()
    # If the company exists.
    if check_team_exists(dao_company, name):
        raise ObjectExistsError("Company ", name + " already exist. "
                                + "Please try with a new name or request "
                                + "to join the team.")
    # if no errors
    try:
        company = Company(name=name, description=desc, ind_id=indust)
        dao_company.add_company(company)
        # TODO: change when there is user in session
        update_tags_from_team_desc(dao_company, dao_tag,
                                   dao_company_tag, desc, name)
        company = dao_company.get_company_by_name(name)
        add_team(mysql, company.tid, uid)
        message = "Registered!"
        return message
    except Exception as e:
        raise e


def add_dummy_companies(mysql: MySQL) -> None:
    """
    Populate Company table with dummy data.
    :param mysql: mysql db.
    """
    epsilon = Company(
        tid=1,
        name="Epsilon",
        description="A startup named Epsilon.",
        create_date=datetime.now())
    delta = Company(
        tid=2,
        name="Delta",
        description="A startup named Delta.",
        create_date=datetime.now())
    companies_to_add = [epsilon, delta]
    dao_company = DAOCompany(mysql)
    dao_tag = DAOTag(mysql)
    dao_company_tag = DAOCompanyTag(mysql)
    for company in companies_to_add:
        dao_company.add_company(company)
        update_tags_from_team_desc(dao_company, dao_tag, dao_company_tag,
                                   company.description, company.name)


def get_company_profile(mysql: MySQL, tid: int) -> Company:
    """
    Return the company object with the same tid.
    :param mysql: mysql db.
    :param tid: tid of the company.
    :return a company object with details from company number tid.
    """
    dao_company = DAOCompany(mysql)
    company = dao_company.get_company_by_tid(tid)
    if company is None:
        raise ObjectNotExistsError("The company")
    return company


def get_company_profile_by_name(mysql: MySQL, name: str) -> Company:
    """
    Return the company object with the same name.
    :param mysql: mysql db.
    :param name: name of the company.
    :return return a company object with details from company with name.
    """
    dao_company = DAOCompany(mysql)
    company = dao_company.get_company_by_name(name)
    if company is None:
        raise ObjectNotExistsError("The company")
    return company


def update_company(mysql: MySQL, tid: int, name: str,
                   description: str) -> str:
    """
    Updates a user with given parameters.
    :param mysql: mysql db.
    :param tid: tid of company.
    :param name: name of user.
    :param description: description of user.
    :param ind_id: industry id of the company.
    :return: Message whether update was successful.
    """
    dao_company = DAOCompany(mysql)
    dao_tag = DAOTag(mysql)
    dao_company_tag = DAOCompanyTag(mysql)
    team_to_update = dao_company.get_company_by_tid(tid)
    if team_to_update is None:
        raise ObjectNotExistsError("The user")
    else:
        team_to_update.name = name
        team_to_update.description = description
        dao_company.update_company(team_to_update)
        update_tags_from_team_desc(dao_company, dao_tag, dao_company_tag, description, name)
        return "Company info updated."


def get_company_owner_by_tid(mysql: MySQL, tid: int) -> User:
    """
    Return the details of the company owner.
    :param mysql: mysql db.
    :param tid: tid of the company.
    :return User object of the company owner.
    """
    user_details = User()
    dao_team = DAOTeam(mysql)
    team = dao_team.get_users_from_team(tid)
    if team is None:
        raise ObjectNotExistsError("The company")
    else:
        for user in team:
            if user.rid == Role.TEAM_OWNER.value:
                user_details = User(name=user.name, contact=user.contact, rid=user.rid, description=user.description)
    return user_details
