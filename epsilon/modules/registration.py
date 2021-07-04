from datetime import datetime
from classes.CompanyTag import CompanyTag
from classes.Tag import Tag
from databaseAccess.DAOCompanyTag import DAOCompanyTag
from databaseAccess.DAOTag import DAOTag
from databaseAccess.DAOIndustry import DAOIndustry
from databaseAccess.DAOTeam import DAOTeam
from databaseAccess.DAOUser import DAOUser
from databaseAccess.DAOCompany import DAOCompany
from flask import Flask, request, render_template
from rake_nltk import Rake
from classes.Company import Company
from classes.Role import Role
from classes.Team import Team
from classes.User import User

# def is_pos_int(s):
#     # EP-1: Team management
#     try:
#         if int(s) > 0:
#             return True
#         else:
#             return False
#     except ValueError:
#         return False


def check_team_exists(dao_company, name):
    # Returns 1 if match is found else returns 0
    company = dao_company.get_company_by_name(name)
    if company:
        if company.name.lower() == name.lower():
            return 1
    return 0


# def registration(mysql):
#     # TODO: check if user is logged in and check permissions
#     # cur = mysql.connection.cursor()
#     dao_company = DAOCompany(mysql)
#     dao_user = DAOUser(mysql)
#     dao_team = DAOTeam(mysql)
#     if request.method == 'POST':
#         # check if all form boxes are completed
#         if (len(request.form['teamname']) == 0 or len(request.form['teamdesc']) == 0):
#             error = 'Please fill in all boxes.'
#             return render_template('registration.html', error=error)
#         # If the company exists.
#         if (check_team_exists(dao_company, request.form['teamname']) == 1):
#             error = 'This company already exists. Please try with a new name or request to join ' + request.form['teamname'] + ' here.'
#             return render_template('registration.html', error=error)
#         # if no errors
#         try:
#             company = Company(name=request.form['teamname'],
#                               description=request.form['teamdesc'])
#             message = dao_company.add_company(company)
#             company = dao_company.get_company_by_name(company.name)

#             joe = User(rid=Role.TEAM_OWNER.value, name="Joe", contact="Jo@gmail.com", password="admin")
#             dao_user.add_user(joe)
#             joe = dao_user.get_user_by_contact("Jo@gmail.com")
#             team = Team(tid=company.tid, uid=joe.uid, rid=Role.TEAM_OWNER.value)
#             dao_team.add_team(team)
#         except Exception as e:
#             return render_template('registration.html', error=e)
#         return render_template('registration.html', message=message)
#     else:
#         # load if not POST
#         return render_template("registration.html")


def is_pos_int(s):
    """
    Checks if the char is a integer or not
    :param s: The character
    :return: Bool based on if the char is int or not.
    """
    # EP-1: Team management
    try:
        if int(s) > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# def check_team_exists(dao, name):
#     """
#     Checks if the team exists.
#     :param dao: The DAO object
#     :param name: the name of the team
#     :return: Returns 1 if match is found else returns 0
#     """
#     # Returns 1 if match is found else returns 0
#     companies = dao.get_companies()
#     for company in companies:
#         if company.name.lower() == name.lower():
#             return 1
#     return 0


def update_tags_from_team_desc(dao_company, dao_tag, dao_company_tag, desc, team_name):
    """
    Adds tags to the database and links them to the team
    :param dao: The DAO object
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


def registration(mysql):
    """
    Renders the template for team registration.
    :param dao: The DAO object
    :return Renders the template for team registration.
    """
    dao_industry = DAOIndustry(mysql)
    dao_company = DAOCompany(mysql)
    dao_user = DAOUser(mysql)
    dao_team = DAOTeam(mysql)
    dao_tag = DAOTag(mysql)
    dao_company_tag = DAOCompanyTag(mysql)
    industry = dao_industry.get_industries()
    if request.method == 'POST':
        # check if all form boxes are completed
        if (len(request.form['teamname']) == 0 or len(request.form['teamdesc']) == 0 or len(
                request.form['industryselect']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('registration.html', error=error, industry=industry)
        # If the company exists.
        if check_team_exists(dao_company, request.form['teamname']) == 1:
            error = 'This company already exists. Please try with a new name or request to join ' + request.form[
                'teamname'] + ' here.'
            return render_template('registration.html', error=error, industry=industry)
        # if no errors
        try:
            company = Company(name=request.form['teamname'],
                              description=request.form['teamdesc'], ind_id=request.form['industryselect'])
            dao_company.add_company(company)
            joe = User(rid=Role.TEAM_OWNER.value, name="Joe", contact="Jo@gmail.com")
            team = Team(tid=3, uid=6, rid=Role.TEAM_OWNER.value)
            update_tags_from_team_desc(dao_company, dao_tag, dao_company_tag, request.form['teamdesc'], request.form['teamname'])
            dao_user.add_user(joe)
            dao_team.add_team(team)
            message = "Registered!"
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message, industry=industry)
    else:
        # load if not POST
        return render_template("registration.html", industry=industry)


def add_dummy_companies(mysql) -> None:
    """
    Populate Company table with dummy data.
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
        update_tags_from_team_desc(dao_company, dao_tag, dao_company_tag, company.description, company.name)