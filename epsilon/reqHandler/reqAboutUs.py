from flask import request, render_template, redirect, url_for


def render_about_us():
    """
    Render the About Us page.
    :return: the template for About Us.
    """
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/aboutUs')]
    return render_template('about_us.html')
