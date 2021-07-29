from epsilonModules.ModJob import apply_to_job, check_existence_of_application
from flask import request, render_template
from flask_login import current_user
import traceback

def render_job_application(mysql: MySQL, jid:int):
    """
    Handler for page where user applies to a specific job.
    This handler assumes current user is eligible to apply for a job.
    :param: mysql: mysql db
    :return: template
    """
    try:
        if request.method == "POST":
            skills = request.form["skills"]
            message = apply_to_job(mysql=mysql, jid=jid, uid=current_user.uid, skills=skills)
            return render_template("job_application.html", message=message)
        else:
            return render_template("job_application.html")

    except Exception as e:
        traceback.print_exc()
        return render_template("job_application.html", error=e)
