from flask import request, render_template
from flask_mysqldb import MySQL

from epsilonModules.ModService import *


def render_services(mysql: MySQL):
    """
    Handler for the services page.
    :param mysql: mysql db.
    :return template for the services page.
    """
    if request.method == "POST":
        # add a service only if you're a service provider
        pass
    else:
        try:
            service_details = get_services(mysql)
            return render_template('services.html', service_details=service_details)
        except Exception as e:
            return render_template('services.html', message=e)