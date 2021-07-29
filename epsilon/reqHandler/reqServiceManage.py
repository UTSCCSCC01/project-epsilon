from flask import request, render_template
from flask_mysqldb import MySQL
from flask_login import current_user

from classes.Type import Type
from epsilonModules.ModService import *
from epsilonModules.ModUser import get_user_by_uid


def render_services(mysql: MySQL):
    """
    Handler for the services page.
    :param mysql: mysql db.
    :return: template for the services page.
    """
    # Check if authenticated user is a service provider to add a service
    uid = -1
    is_service_provider = False
    message = ""

    if current_user.is_authenticated:
        uid = current_user.uid
        user = get_user_by_uid(mysql, uid)
        if user.type_id == Type.SERVICE_PROVIDER.value:
            is_service_provider = True

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
            return render_template('services.html', error=e)

    try:
        service_details = get_services(mysql)
        return render_template('services.html', service_details=service_details,
                               is_service_provider=is_service_provider, message=message)
    except Exception as e:
        return render_template('services.html', error=e)