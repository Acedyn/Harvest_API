from flask import Blueprint, jsonify
from sqlalchemy import func
from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job

# Initialize the set to routes for infos
stats = Blueprint("stats", __name__)

# Set of filter to get rig of unused pools
pool_filters = (
    Blade.profile != "LAVIT",
    Blade.profile != "JV",
    Blade.profile != "windows10",
    Blade.profile != "TD",
    Blade.profile != "BUG",
    Blade.availdisk > 5
)

# Return the amound of blades that are working, free, and on nimby
@stats.route("/stats/blades-status")
def blades_status():
    # Get the working blades
    blades_busy = sessions["tractor"].query(func.count(1)) \
    .filter(BladeUse.taskcount > 0) \

    # Get the free blades
    blades_free = sessions["tractor"].query(func.count(Blade.bladeid)) \
    .filter(Blade.status == "") \
    .filter(*pool_filters) \

    # Get the blades with nimby on
    blades_nimby = sessions["tractor"].query(func.count(1)) \
    .filter(Blade.status.like("nimby%") ) \
    .filter(*pool_filters) \

    # Get the blades that are off
    # TODO: find the sqlalchemy way to use the function age
    blades_off_query = engines["tractor"].execute("SELECT count(*) FROM blade where age(current_timestamp, heartbeattime) > interval '1 hours'")
    blades_off = [blades_off_result[0] for blades_off_result in blades_off_query]

    # Return a json
    response = [{"name": "Free", "value": blades_free[0][0]}, {"name": "Busy", "value": blades_busy[0][0]}, {"name": "Nimby ON", "value": blades_nimby[0][0]}, {"name": "Off", "value": blades_off[0]}]
    return jsonify(response)


# Return how many blades each projects are occupying
@stats.route("/stats/projects-usage")
def projects_usage():
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
