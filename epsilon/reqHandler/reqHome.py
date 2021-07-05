from flask import Flask, request, render_template, redirect, url_for
from flask_mysqldb import MySQL


def render_home():
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('home.html')


def render_previous_home():
    global baseUrl
    baseUrl = request.base_url[:request.base_url.rfind('/previousHome')]
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('previousHome.html')
