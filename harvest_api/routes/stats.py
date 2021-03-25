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
def get_blades_status():
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

    return blades_free[0][0], blades_busy[0][0], blades_nimby[0][0], blades_off[0][0]

@stats.route("/stats/blades-status")
def blades_status():
    # TODO: Find a cleaner way to to this
    # This is to reuse the get_blades_status function in tractor_history.py
    blades_free, blades_busy, blades_nimby, blades_off = get_blades_status()

    # Return a json
    response = [{"name": "Free", "value": blades_free}, 
        {"name": "Busy", "value": blades_busy}, 
        {"name": "Nimby ON", "value": blades_nimby}, 
        {"name": "Off", "value": blades_off}]

    return jsonify(response)

# Return how many blades each projects are occupying
def get_projects_usage():
    # Get the working blades
    blades_busy = sessions["tractor"].query(BladeUse.owners, func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(days=10)) \
    .filter(BladeUse.taskcount == 1) \
    .filter(func.array_length(BladeUse.owners, 1) == 1) \
    .group_by(BladeUse.owners)

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_busy in blades_busy:
        response.append({"name": blade_busy[0][0], "value": blade_busy[1]})

    return response

@stats.route("/stats/projects-usage")
def projects_usage():
    # TODO: Find a cleaner way to to this
    # This is to reuse the get_projects_usage function in tractor_history.py
    blades_busy = get_projects_usage()
    return jsonify(blades_busy)

# Return how many blades are running for each blade types
def get_blades_usage():
    # Get the working blades
    blades_busy = sessions["tractor"].query(func.regexp_matches(Blade.name, "mk[0-9]*", "g"), func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(days=10)) \
    .filter(BladeUse.taskcount == 1) \
    .filter(func.array_length(func.regexp_matches(Blade.name, "mk[0-9]*", "g")) > 0) \
    .group_by(func.regexp_matches(Blade.name, "mk[0-9]*", "g"))

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_busy in blades_busy:
        response.append({"name": blade_busy[0][0], "value": blade_busy[1]})

    return response

@stats.route("/stats/blades-usage")
def blades_usage():
    # TODO: Find a cleaner way to to this
    # This is to reuse the get_blades_usage function in tractor_history.py
    blades_busy = get_blades_usage()
    return jsonify(blades_busy)

# Return the historic of the blades use
@stats.route("/stats/blades-history")
def blades_history():
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

# Return the historic of the blades use from a starting date
@stats.route("/stats/blades-history/<int:date>")
def blades_history_date(date):
    starting_date = datetime.datetime.fromtimestamp(int(date))

    # Get the historic of the blades
    blades_history = sessions["harvest"].query( \
        func.extract("hour", History.date), \
        func.avg(History.blade_busy).label("busy"), \
        func.avg(History.blade_nimby).label("nimby"), \
        func.avg(History.blade_off).label("off"), \
        func.avg(History.blade_free).label("free")) \
    .filter(History.date >= starting_date) \
    .group_by(func.extract("hour", History.date)) \
    .order_by(func.extract("hour", History.date)) \

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_history in blades_history:
        response.append({"time": blade_history[0], "busy": float(blade_history[1]), "nimby": float(blade_history[2]), "off": float(blade_history[3]), "free": float(blade_history[4])})

    # Return the response in json format
    return jsonify(response)
