from epsilonModules.ModTeam import get_user_teams
from epsilonModules.ModUser import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Service import *
from epsilonModules.ModService import *


def render_user_profile(mysql: MySQL):
    """
    Handler for user profile.
    :param mysql: mysql db.
    :return template for user profile page.
    """
    uid = current_user.uid
    message = ""
    try:
        tid = -1
        if request.method == 'POST':
            data = request.get_json
            if "action" in request.form:
                action = request.form["action"].split("_")
                if action[0] == "E":
                    sid=action[1]
                    stid=action[2]
                    if "type" in request.form:
                        stid=request.form['type']
                    title = request.form['title']
                    description = request.form['description']
                    price = request.form['price']
                    link = request.form['link']
                    service = Service(sid,uid,stid,title,description,price,link)
                    message = edit_service(mysql,Service)
                elif action[0] == "R":
                    message = remove_service(mysql,action[1])
            elif data:
                name = request.form["name"]
                description = request.form["description"]
                contact = request.form["contact"]
                message = update_user(mysql, uid, name,
                                      description, contact)
        user_details = get_user_profile(mysql, uid)
        services = get_services_by_uid(mysql,uid)
        if current_user.is_authenticated:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('user_profile.html', user_details=user_details,
                               message=message, tid=tid, services=services)
    except ObjectNotExistsError as e:
        return render_template('user_profile.html', user_details=None,
                               message=message, tid= tid)
    except Exception as e:
        return render_template('user_profile.html', message=e)

def load_User_O(mysql: MySQL, uid: int):
    """
    Returns a user object to be verified by the session
    :param mysql: mysql db.
    :param uid: uid of user
    :return user object.
    """
    user = get_user_by_uid(mysql, uid)
    return user


def user_services(mysql:MySQL):
    """
    Renders the template for services provided by the user
    """
    uid = current_user.uid
    message = ""
    try:
        print(1)
        tid = -1
        if request.method == 'POST':
            print(request.form)
            action = request.form["action"].split("_")
            print(3)
            if action[0] == "E":
                print(4)
                sid=action[1]
                stid=action[2]
                print(5)
                if "type" in request.form:
                    print(6)
                    stid=request.form['type']
                title = request.form['title']
                description = request.form['description']
                price = request.form['price']
                link = request.form['link']
                service = Service(sid,uid,stid,title,description,price,link)
                print(7)
                message = edit_service(mysql,service)
                print(8)
            elif action[0] == "R":
                print(9)
                message = remove_service(mysql,action[1])
                print(10)
            elif action[0] =="A":
                print(11)
                title = request.form['title']
                description = request.form['description']
                price = request.form['price']
                link = request.form['link']
                service_type = None
                if "type" in request.form:
                    service_type = request.form["type"]
                message = add_service (mysql, uid, title, description, price, link, service_type)
                print(12)
        services = get_services_by_uid(mysql, uid)
        print(13)
        return render_template("user_services.html", message=message, tid=tid, services=services)
    except Exception as e:
        return render_template("user_services.html", message=e, tid=-1)