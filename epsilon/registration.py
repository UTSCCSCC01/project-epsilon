from flask import request, render_template
from rake_nltk import Rake

from classes.Company import Company
from classes.CompanyTags import CompanyTags
from classes.Role import Role
from classes.Tags import Tags
from classes.Team import Team
from classes.User import User


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


def check_team_exists(dao, name):
    """
    Checks if the team exists.
    :param dao: The DAO object
    :param name: the name of the team
    :return: Returns 1 if match is found else returns 0
    """
    # Returns 1 if match is found else returns 0
    companies = dao.get_companies()
    for company in companies:
        if company.name.lower() == name.lower():
            return 1
    return 0


def update_tags_from_team_desc(dao, desc, team_name):
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
    companies = dao.get_companies()
    tid = 0
    for team in companies:
        if team.name == team_name:
            tid = team.tid
            break
    for keywords in keyword_extracted:
        tags = Tags(name=keywords)
        dao.add_tags(tags)
        tag = dao.get_tag(keywords)
        company_tags = CompanyTags(tag_id=tag.tag_id, tid=tid)
        dao.add_company_tags(company_tags)


def registration(dao):
    """
    Renders the template for team registration.
    :param dao: The DAO object
    :return Renders the template for team registration.
    """
    industry = dao.get_industry()
    if request.method == 'POST':
        # check if all form boxes are completed
        if (len(request.form['teamname']) == 0 or len(request.form['teamdesc']) == 0 or len(
                request.form['industryselect']) == 0):
            error = 'Please fill in all boxes.'
            return render_template('registration.html', error=error, industry=industry)
        # If the company exists.
        if check_team_exists(dao, request.form['teamname']) == 1:
            error = 'This company already exists. Please try with a new name or request to join ' + request.form[
                'teamname'] + ' here.'
            return render_template('registration.html', error=error, industry=industry)
        # if no errors
        try:
            company = Company(name=request.form['teamname'],
                              description=request.form['teamdesc'], ind_id=request.form['industryselect'])
            dao.add_company(company)
            joe = User(rid=Role.TEAM_OWNER.value, name="Joe", contact="Jo@gmail.com")
            team = Team(tid=3, uid=6, rid=Role.TEAM_OWNER.value)
            update_tags_from_team_desc(dao, request.form['teamdesc'], request.form['teamname'])
            dao.add_user(joe)
            dao.add_team(team)
            message = "Registered!"
        except Exception as e:
            return render_template('registration.html', error=e)
        return render_template('registration.html', message=message, industry=industry)
    else:
        # load if not POST
        return render_template("registration.html", industry=industry)
