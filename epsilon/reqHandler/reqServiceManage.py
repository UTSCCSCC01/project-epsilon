from epsilonModules.ModTeam import get_user_teams
from flask import request, render_template
from flask_mysqldb import MySQL
from flask_login import current_user
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from classes.Type import Type
from epsilonModules.ModService import *
from epsilonModules.ModUser import get_user_by_uid


def filter_services(service_details: list, fltr: str):
    ret_value = []
    if fltr == "All":
        return service_details
    for item in service_details:
        if item[2].lower() == fltr.lower():
            ret_value.append(item)
    return ret_value


def render_services(mysql: MySQL):
    """
    Handler for the services page.
    :param mysql: mysql db.
    :return: template for the services page.
    """
    # Check if authenticated user is a service provider to add a service
    uid = -1
    tid = -1
    is_service_provider = False
    message = ""

    if current_user.is_authenticated:
        uid = current_user.uid
        user = get_user_by_uid(mysql, uid)
        if user.type_id == Type.SERVICE_PROVIDER.value:
            is_service_provider = True
        elif user.type_id == Type.STARTUP_USER.value:
            try:
                user_teams = get_user_teams(mysql, current_user.uid)
                tid = user_teams[0].tid
            except ObjectNotExistsError as oe:
                pass

    if request.method == "POST":
        try:
            title = request.form['title']
            description = request.form['description']
            price = request.form['price']
            link = request.form['link']
            service_type = None
            if 'type' in request.form:
                service_type = request.form['type']
            message = add_service(mysql, uid, title, description, price, link, service_type)
        except Exception as e:
            return render_template('services.html', error=e, tid=tid)

    try:
        flt = request.args.get("filter")
        service_details = get_services(mysql)
        filtered_service_details = service_details
        if flt:
            filtered_service_details = filter_services(service_details, flt)
        else:
            flt = "All"

        return render_template('services.html', service_details=service_details,
                               is_service_provider=is_service_provider, message=message,
                               filtered_service_details=filtered_service_details, flt=flt, tid=tid)
    except Exception as e:
        return render_template('services.html', error=e, tid=tid)
