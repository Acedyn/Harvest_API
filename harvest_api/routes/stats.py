import datetime
from flask import Blueprint, jsonify
from sqlalchemy import func
from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job
from mappings.harvest_tables import History

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
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount > 0)
    
    # Get the free blades
    blades_free = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status == "")  \
    .filter(Blade.nimby == "") 

    # Get the blades with nimby on
    blades_nimby = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status.like("%nimby%"))

    # Get the blades that are off
    blades_off = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(BladeUse.taskcount == 0) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) > datetime.timedelta(seconds=180)) \

    # Return a json
    response = [{"name": "Free", "value": blades_free[0][0]}, {"name": "Busy", "value": blades_busy[0][0]}, {"name": "Nimby ON", "value": blades_nimby[0][0]}, {"name": "Off", "value": blades_off[0][0]}]
    return jsonify(response)


# Return how many blades each projects are occupying
@stats.route("/stats/projects-usage")
def projects_usage():
    # Get the working blades
    blades_busy = sessions["tractor"].query(BladeUse.owners, func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount > 0) \
    .group_by(BladeUse.owners)

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_busy in blades_busy:
        response.append({"name": blade_busy[0], "value": blade_busy[1]})

    # Return the response in json format
    return jsonify(response)


# Return the historic of the blades use
@stats.route("/stats/blades-history")
def blades_historic():
    # Get the historic of the blades
    blades_history = sessions["harvest"].query( \
        func.extract("hour", History.date), \
        func.avg(History.blade_busy).label("busy"), \
        func.avg(History.blade_nimby).label("nimby"), \
        func.avg(History.blade_off).label("off"), \
        func.avg(History.blade_free).label("free")) \
    .group_by(func.extract("hour", History.date)) \
    .order_by(func.extract("hour", History.date)) \

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_history in blades_history:
        response.append({"time": blade_history[0], "busy": float(blade_history[1]), "nimby": float(blade_history[2]), "off": float(blade_history[3]), "free": float(blade_history[4])})

    # Return the response in json format
    return jsonify(response)
