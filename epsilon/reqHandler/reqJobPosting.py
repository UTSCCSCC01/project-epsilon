from flask_mysqldb import MySQL
from exceptions.ObjectNotExistsError import ObjectNotExistsError
from epsilonModules.ModJob import validate_team_admin, validate_startup_user,\
    reverse_status_of_job_posting, get_job_postings_by_tid,\
    post_job, get_tid_by_admin_uid, apply_to_job
from flask import request, render_template, redirect, url_for
from flask_login import current_user
from classes.Type import Type
import sys, traceback

def render_job_posting_management(mysql: MySQL):
    """
    Handler for page where team admins can manage all
    job postings within the company.
    Also contains link for posting new jobs.
    :param: mysql: mysql db
    :return: template
    """
    try:
        tids_under_curr_user = get_tid_by_admin_uid(mysql=mysql, uid=current_user.uid)
        if request.method == 'POST':
            if request.form["update_posting_action"]:   # if one has clicked the button
                update_posting_action = request.form["update_posting_action"].split("_")
                if update_posting_action[0] == 'R':
                    # mysql, jid
                    reverse_status_of_job_posting(mysql, update_posting_action[1])

        # default to the first company managed by current user
        postings = get_job_postings_by_tid(mysql, tids_under_curr_user[0])
        postings_lst = []
        for p in postings:
            postings_lst.append((p.title, p.description, p.create_date, p.active, p.jid))
        return render_template("job_posting_mgmt.html",
                                job_postings=postings_lst)
    except Exception as e:
        traceback.print_exc()
        return render_template("job_posting_mgmt.html", error=e)


def render_job_postings_by_company(mysql: MySQL, company_tid: int):
    """
    Handler for page for all job postings that only startup
    users can see and apply to jobs.
    :param: mysql: mysql db
    :return: template
    """
    try:
        validate_startup_user(current_user.type_id)
        postings = get_job_postings_by_tid(mysql, company_tid)
        postings_lst = []
        for p in postings:
            postings_lst.append((p.title, p.description, p.create_date, p.active, str(p.jid)))
        return render_template("job_postings_of_company.html",
                                   job_postings=postings_lst)
    except Exception as e:
        return render_template("job_postings_of_company.html", error=e)


def render_post_new_job(mysql: MySQL):
    """
    Handler for posting a new job.
    :param: mysql: mysql db
    :return: template
    """
    tids_under_curr_user = get_tid_by_admin_uid(mysql=mysql, uid=current_user.uid)
    team_id = tids_under_curr_user[0]
    try:
        if request.method == 'POST':
            title = request.form["title"]
            description = request.form["description"]
            message = post_job(mysql=mysql, tid=team_id, title=title,
                              description=description)
            return render_template("post_new_job.html",
                                    message=message)
        else:
            return render_template("post_new_job.html")

    except Exception as e:
        return render_template("post_new_job.html", error=e)


def render_job_application(mysql: MySQL, job_id: int):
    """
    Handler for applying to a new job.
    The function assumes the currently logged in user is a startup user.
    :param: mysql: mysql db
    :return: template
    """
    try:
        if request.method == 'POST':
            skills = request.form["skills"]
            message = apply_to_job(mysql=mysql, jid=job_id,
                                   uid=current_user.uid, skills=skills)
            return render_template("job_application.html",
                                    message=message)
        else:
            return render_template("job_application.html")

    except Exception as e:
        return render_template("job_application.html", error=e)