from werkzeug.utils import secure_filename
from epsilonModules.ModTeam import get_user_teams
from epsilonModules.ModUser import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Service import *
from epsilonModules.ModService import *
import os
from epsilonModules.ModPic import *



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
                    message = edit_service(mysql,service)
                elif action[0] == "R":
                    message = remove_service(mysql,action[1])
                elif action[0] =="A":
                    title = request.form['title']
                    description = request.form['description']
                    price = request.form['price']
                    link = request.form['link']
                    service_type = None
                    if "type" in request.form:
                        service_type = request.form["type"]
                    message = add_service (mysql, uid, title, description, price, link, service_type)
            elif data:
                name = request.form["name"]
                description = request.form["description"]
                contact = request.form["contact"]
                message = update_user(mysql, uid, name,
                                      description, contact)
                if 'pfpi' in request.files:
                    f = request.files['pfpi']
                    file = f.stream.read()
                    if get_pic(mysql,uid) is not None:
                        edit_pic(mysql,uid,file)
                    else:
                        add_pic(mysql,uid,file)
        pfp = get_pic(mysql, uid)
        if pfp:
            if os.path.exists("./static/pfp.png"):
                os.remove("./static/pfp.png")
            with open('./static/pfp.png', 'wb') as wf:
                wf.write(pfp)
        user_details = get_user_profile(mysql, uid)
        services = get_services_by_uid(mysql,uid)
        if current_user.is_authenticated and current_user.type_id == 1:
            user_teams = get_user_teams(mysql, current_user.uid)
            tid = user_teams[0].tid
        return render_template('user_profile.html', user_details=user_details,
                               message=message, tid=tid, services=services,
                               pic=pfp)
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
        tid = -1
        if request.method == 'POST':
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
                message = edit_service(mysql,service)
            elif action[0] == "R":
                message = remove_service(mysql,action[1])
            elif action[0] =="A":
                title = request.form['title']
                description = request.form['description']
                price = request.form['price']
                link = request.form['link']
                service_type = None
                if "type" in request.form:
                    service_type = request.form["type"]
                message = add_service (mysql, uid, title, description, price, link, service_type)
        services = get_services_by_uid(mysql, uid)
        return render_template("user_services.html", message=message, tid=tid, services=services)
    except Exception as e:
        return render_template("user_services.html", message=e, tid=-1)