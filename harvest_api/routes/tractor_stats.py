from flask import Blueprint
from flask import jsonify
from sqlalchemy import func
from database import sessions
from mappings.tractor_tables import Blade, Task, Job

# Initialize the set to routes for tractor
tractor_stat = Blueprint("tractor_stat", __name__)


# Route for "/pc-work"
@tractor_stat.route("/pc-work")
def pc_work():
    # Get the working blades
    blades_busy = sessions["tractor"].query(func.count(Job.jid)) \
    .filter(Job.jid == Task.jid) \
    .filter(Task.state == "active") \

    # Get the free blades
    blades_free = sessions["tractor"].query(func.count(Blade.bladeid)) \
    .filter(Blade.status == "")

    # Get the blades with nimby on
    blades_nimby = sessions["tractor"].query(func.count(Blade.bladeid)) \
    .filter(Blade.nimby != "")

    # .filter(Blade.profile != "LAVIT") \
    # .filter(Blade.profile != "JV") \
    # .filter(Blade.profile != "windows10") \
    # .filter(Blade.profile != "TD") \
    # .filter(Blade.profile != "BUG") \
    # .filter(Blade.availdisk > 5).count()

    # Return a json
    response = [{"name": "Free", "value": blades_free[0][0]}, {"name": "Busy", "value": blades_busy[0][0]}, {"name": "Nimby ON", "value": blades_nimby[0][0]}]
    return jsonify(response)

# Route for "/pc-crew"
@tractor_stat.route("/pc-crew")
def pc_crew():
    # Get the working blades per project
    blades_busy = sessions["tractor"].query(Job.owner, func.count(Job.owner)) \
    .filter(Job.jid == Task.jid) \
    .filter(Task.state == "active") \
    .group_by(Job.owner)

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_busy in blades_busy:
        response.append({"name": blade_busy[0], "value": blade_busy[1]})

    # Return the response in json format
    return jsonify(response)
