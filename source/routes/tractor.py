from flask import Blueprint
from mappings.tractor import Job
from server import tractor_db

tractor_routes = Blueprint("main", __name__)

@tractor_routes.route("/")
def index():
    job_query = tractor_db.session.query(Job.jid, Job.owner).order_by(Job.jid).all()
    for job_responce in job_query:
        print(job_responce)

    return "Hello World !"
