from flask import request, render_template, redirect, url_for


def render_home():
    """
    Render the home page.
    :return: the template for home page.
    """
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('home.html')


def render_previous_home():
    """
    Render the old version of home page.
    :return: the template for previous home page.
    """
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/previousHome')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('previous_home.html')
