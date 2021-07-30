from flask import request, render_template, redirect, url_for


def render_resources():
    """
    Render the Resources page.
    :return: the template for Resources.
    """
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/resources')]
    return render_template('resources.html')
