import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job
from mappings.harvest_tables import HistoryFarm, HistoryProject, HistoryBlade, Project, HistoryTotalCompute

# Initialize the set to routes for infos
stats = Blueprint("stats", __name__)

# Set of filter to get rig of unused pools
pool_filters = (
    Blade.profile != "LAVIT",
    Blade.profile != "windows10",
    Blade.profile != "TD",
    Blade.profile != "BUG",
    Blade.availdisk > 5
)

# Set of filters for profiles
profile_filters = or_(
    func.upper(Blade.profile).like("MK%"),
    func.upper(Blade.profile).like("RACK-%"),
    func.upper(Blade.profile) == "JV",
    func.upper(Blade.profile) == "TD",
    func.upper(Blade.profile) == "VRAYMISSING",
    func.upper(Blade.profile) == "MULTIFCT",
    func.upper(Blade.profile) == "WINDOWS10",
)

# Return the amound of blades that are working, free, and on nimby
def get_farm_status():
    # Get the working blades
    blades_busy = sessions["tractor"].query(func.count(1)) \
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount > 0)
    
    # Get the free blades
    blades_free = sessions["tractor"].query(func.count(1)) \
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status == "")  \
    .filter(Blade.nimby == "") 

    # Get the blades with nimby on
    blades_nimby = sessions["tractor"].query(func.count(1)) \
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status.like("%nimby%"))

    # Get the blades that are off
    blades_off = sessions["tractor"].query(func.count(1)) \
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(BladeUse.taskcount == 0) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) > datetime.timedelta(seconds=180)) \

    return blades_free[0][0], blades_busy[0][0], blades_nimby[0][0], blades_off[0][0]

@stats.route("/stats/blades-status")
def blades_status():
    # TODO: Find a cleaner way to to this
    # This is to reuse the get_blades_status function in tractor_history.py
    blades_free, blades_busy, blades_nimby, blades_off = get_farm_status()

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
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(minutes=180)) \
    .filter(BladeUse.taskcount > 0) \
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
    blades_busy = sessions["tractor"].query(func.regexp_matches(func.upper(Blade.name), "MK[0-9]*", "g"), func.count(1)) \
    .filter(profile_filters) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount > 0) \
    .group_by(func.regexp_matches(func.upper(Blade.name), "MK[0-9]*", "g"))

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

# Return the historic of the blades use along a day from a starting and end date
@stats.route("/stats/farm-history/hours")
def farm_history_hours():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    ignore_weekend = request.args.get('ignore-we', default = False, type = bool)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # List of filters that will be added according to some parameters in the route
    optional_filters = []
    # If the 'we' parameter in the route is true
    if ignore_weekend:
        optional_filters.append(func.extract("dow", HistoryFarm.date) != 0)
        optional_filters.append(func.extract("dow", HistoryFarm.date) != 6)
        
    # Get the historic of the blades
    blades_history = sessions["harvest"].query( \
        func.extract("hour", HistoryFarm.date), \
        func.avg(HistoryFarm.blade_busy).label("busy"), \
        func.avg(HistoryFarm.blade_nimby).label("nimby"), \
        func.avg(HistoryFarm.blade_off).label("off"), \
        func.avg(HistoryFarm.blade_free).label("free")) \
    .filter(HistoryFarm.date >= starting_date) \
    .filter(HistoryFarm.date <= ending_date) \
    .filter(*optional_filters) \
    .group_by(func.extract("hour", HistoryFarm.date)) \
    .order_by(func.extract("hour", HistoryFarm.date)) \

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_history in blades_history:
        response.append({"time": blade_history[0], "busy": float(blade_history[1]), "nimby": float(blade_history[2]), "off": float(blade_history[3]), "free": float(blade_history[4])})

    # Return the response in json format
    return jsonify(response)

# Return the historic of the blades use along a week from a starting and end date
@stats.route("/stats/farm-history/days")
def farm_history_days():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # Get the history of the farm
    farm_history = sessions["harvest"].query( \
        func.extract("dow", HistoryFarm.date), \
        func.avg(HistoryFarm.blade_busy).label("busy"), \
        func.avg(HistoryFarm.blade_nimby).label("nimby"), \
        func.avg(HistoryFarm.blade_off).label("off"), \
        func.avg(HistoryFarm.blade_free).label("free")) \
    .filter(HistoryFarm.date >= starting_date) \
    .filter(HistoryFarm.date <= ending_date) \
    .group_by(func.extract("dow", HistoryFarm.date)) \
    .order_by(func.extract("dow", HistoryFarm.date)) \

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_history in farm_history:
        response.append({"time": (blade_history[0] - 1) % 7, 
            "busy": float(blade_history[1]), 
            "nimby": float(blade_history[2]), 
            "off": float(blade_history[3]), 
            "free": float(blade_history[4])})

    # Return the response in json format
    return jsonify(response)

# Return the usage of each project of the farm
@stats.route("/stats/projects-history")
def projects_history():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # Get the history of the projects
    projects_history = sessions["harvest"].query( \
        HistoryProject.date, \
        Project.name, \
        HistoryProject.blade_busy) \
    .filter(HistoryProject.project_id == Project.id) \
    .filter(HistoryProject.date >= starting_date) \
    .filter(HistoryProject.date <= ending_date) \
    .order_by(HistoryProject.date)

    # Initialize the final response that will contain all the timestamps
    response = []
    # If the sql result is empty return nothing
    if len(projects_history.all()) < 1:
        return jsonify(response)
    # Initialize the response buffer
    response_buffer = {"time": projects_history[0][0].timestamp() * 1000}

    # Loop over all the rows of the sql response
    for project_history in projects_history:
        # If a new date is reached
        if project_history[0].timestamp() * 1000 != response_buffer["time"]:
            # Append the response
            response.append(response_buffer.copy())
            # Reinitialise the buffer
            response_buffer = {"time": project_history[0].timestamp() * 1000}
        
        # Add the project name to the buffer
        response_buffer[project_history[1]] = project_history[2]
       
    # Append the response one last time
    response.append(response_buffer.copy())

    # Return the response in json format
    return jsonify(response)

# Return the average total time of computation of the farm over an hour
@stats.route("/stats/blades-history/hour")
def blades_history_hour():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # Get the history of the blades compute time
    blades_history = sessions["harvest"].query( \
        HistoryBlade.blade, \
        func.avg(HistoryBlade.computetime)) \
    .filter(HistoryBlade.date >= starting_date) \
    .filter(HistoryBlade.date <= ending_date) \
    .group_by(HistoryBlade.blade)

    # Initialize the final response that will contain all the timestamps
    response = []

    # Loop over all the rows of the sql response
    for blade_history in blades_history:
        # Append the response
        response.append({"name": blade_history[0], "computetime": blade_history[1].total_seconds() * 1000})
        
    # Return the response in json format
    return jsonify(response)

# Return the average time of computation for each computer types per day
@stats.route("/stats/blades_history/day")
def blades_history_day():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # Get the history of the blades compute time
    blades_history = sessions["harvest"].query( \
        HistoryBlade.blade, \
        func.sum(HistoryBlade.computetime)) \
    .filter(HistoryBlade.date >= starting_date) \
    .filter(HistoryBlade.date <= ending_date) \
    .group_by(func.extract("day", HistoryFarm.date), HistoryBlade.blade)
    
    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    for blade_history in blades_history:
        response.append({"time": (blade_history[0] - 1) % 7, 
            "busy": float(blade_history[1]), 
            "nimby": float(blade_history[2]), 
            "off": float(blade_history[3]), 
            "free": float(blade_history[4])})

    # Return the response in json format
    return jsonify(response)

# Return the total time of computation for each teams
@stats.route("/stats/total-computetime")
def total_computetime():
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = datetime.datetime.timestamp(datetime.datetime.now())*1000, type = int)
    starting_date = datetime.datetime.fromtimestamp(int(start/1000))
    ending_date = datetime.datetime.fromtimestamp(int(end/1000))

    # Get the history of the blades compute time
    total_computetime = sessions["harvest"].query( \
        Project.name, \
        func.sum(HistoryTotalCompute.total_compute)) \
    .filter(HistoryTotalCompute.date >= starting_date) \
    .filter(HistoryTotalCompute.date <= ending_date) \
    .filter(HistoryTotalCompute.project_id == Project.id) \
    .group_by(Project.name).all()

    # Initialize the final response that will contain all the projects
    response = []

    # Loop over all the rows of the sql response
    all_groups = int(0)
    for project_computetime in total_computetime:
        response.append({"project": project_computetime[0], "hours": int(project_computetime[1]/60), "minutes": project_computetime[1]%60})
        all_groups += project_computetime[1]
    
    response.append({"project": "TOTAL", "hours": int(all_groups/60), "minutes": all_groups%60})

    # Return the response in json format
    return jsonify(response)
