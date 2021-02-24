from flask import Blueprint
from flask import jsonify
from mappings.tractor import Job
from server import tractor_db
from sqlalchemy.sql import text
import datetime

tractor_routes = Blueprint("main", __name__)

@tractor_routes.route("/")
def index():
    file = open("G:/PROJECT/2021/TOOL_HarverstBackend/source/query/crew_progression.sql")
    query = text(file.read())
    results = tractor_db.engine.execute(query)

    projects = {
        "date": str(datetime.date(1, 1, 1)),
        "timestamp": 0,
        "DIVE": 0,
        "BARNEY": 0,
        "RELATIVITY": 0,
        "BACKSTAGE": 0,
        "COCORICA": 0,
        "DREAMBLOWER": 0,
        "PIR_HEARTH": 0
    }

    response = []

    for result in results:
        project = result[0]
        date = str(datetime.date(result[1].year, result[1].month, result[1].day))
        timestamp = int(result[1].timestamp())
        done = result[2]

        if(projects["timestamp"] == 0):
            projects["timestamp"] = timestamp
            projects["date"] = date
        elif(projects["timestamp"] != timestamp):
            response.append(projects.copy())
            projects["timestamp"] = timestamp
            projects["date"] = date

        projects[project] = done

    response.append(projects.copy())

    return jsonify(response)
