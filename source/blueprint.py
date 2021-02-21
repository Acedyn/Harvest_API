from flask import Blueprint
from mapping.tractor import Job

blueprint = Blueprint("main", __name__)

@blueprint.route("/")
def index():
    job_query = tractor_db.session.query(Job.jid, Job.owner).order_by(Job.jid).all()
    for job_responce in job_query:
        print(job_responce)

    return "Hello World !"
