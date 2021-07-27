import json
from epsilonModules.ModTeam import *
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Type import Type
import sys, traceback


def render_job_posting_management(mysql: MySQL):
    """
    Handler for page where team admins can manage all
    job postings within the company.
    :param: mysql: mysql db
    :return: template
    """
    pass