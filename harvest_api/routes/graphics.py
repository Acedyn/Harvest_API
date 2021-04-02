from flask import Blueprint, jsonify
from sqlalchemy import func
from sqlalchemy.sql import select, and_, true, false
from database import execute_from_file, sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer, HistoryFarm
from routes.infos import get_projects_infos
import re, datetime

# Initialize the set to routes for tractor
graphics = Blueprint("graphics", __name__)

# Set of filter that we will use multiple times
combine_filters = (
    Layer.frame_id == Frame.id,
    Frame.shot_id == Shot.id,
    Shot.sequence_id == Sequence.id,
    Sequence.project_id == Project.id,
)

# Route to get the progression of the specified project
@graphics.route("/graphics/progression/<project>")
def crew_progression(project):
    # Query all the layers of the given project to get the project name
    project_query = select([func.date_trunc("day", Layer.validation_date), func.count(1).label("frame_count")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        Layer.valid == true(), \
        Layer.validation_date != None,\
        *combine_filters)). \
        group_by(func.date_trunc("day", Layer.validation_date)).\
        order_by(func.date_trunc("day", Layer.validation_date))
    # Execute the query
    results = engines["harvest"].execute(project_query)

    # Initialize the final response that will contain all the timestamps
    response = []
    # Initialize the count of frame rendered
    frame_count = 0

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        date = str(datetime.date(result[0].year, result[0].month, result[0].day))
        timestamp = int(result[0].timestamp()) * 1000
        frame_count += result[1]

        timetamp_state = {"timestamp": timestamp, "date": date, re.sub("-", '_', project.upper()): frame_count}

        response.append(timetamp_state)

    # Return the response in json format
    return jsonify(response)


# Route to get the progression of all the projects
@graphics.route("/graphics/progression")
def projects_progression():
    # Get all the project
    get_project_names = select([Project.name])
    # Execute the query
    projects_names = engines["harvest"].execute(get_project_names)

    # Query all the layers of each projects
    project_query = select([Project.name, func.date_trunc("day", Layer.validation_date), func.count(1).label("frame_count")]) \
        .where(and_( \
        Layer.valid == true(), \
        Layer.validation_date != None,\
        *combine_filters)). \
        group_by(Project.name, func.date_trunc("day", Layer.validation_date)).\
        order_by(func.date_trunc("day", Layer.validation_date), Project.name)
    # Execute the query
    results = engines["harvest"].execute(project_query)


    # Initialize the timestamp_state
    timetamp_state = {
        "timestamp": 0,
    }
    # Initialize all the projects to 0
    for project_name in projects_names:
        timetamp_state[project_name[0]] = 0

    # Initialize the final response that will contain all the timestamps
    response = []

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        project = result[0]
        timestamp = int(result[1].timestamp()) * 1000
        done = result[2]

        # If this the timestamp_state is not initialized yet
        if(timetamp_state["timestamp"] == 0):
            # Initialize the timestamp an the date
            timetamp_state["timestamp"] = timestamp
        # If we reach a new timestamp
        elif(timetamp_state["timestamp"] != timestamp):
            # Store the curent state of timestamp_state in the response
            response.append(timetamp_state.copy())
            timetamp_state["timestamp"] = timestamp

        # Store the value of the row to the current timestamp_state
        timetamp_state[project] += done

    # Append the timestamp_state one last time
    response.append(timetamp_state.copy())

    # Return the response in json format
    return jsonify(response)


# Route to get the history of farm usage
@graphics.route("/graphics/blade-status")
def blades_status_history():
    # Query all the layers of the given project to get the project name
    history_query = select([HistoryFarm.blade_busy, HistoryFarm.blade_off, HistoryFarm.blade_free, HistoryFarm.blade_nimby, HistoryFarm.date]) \
        .order_by(HistoryFarm.date)
    # Execute the query
    results = engines["harvest"].execute(history_query)

    # Initialize the final response that will contain all the timestamps
    response = []

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        timestamp = int(result[4].timestamp()) * 1000
        # Gather all the data of the row
        timetamp_state = {"timestamp": timestamp, "busy": result[0], "off": result[1], "free": result[2], "nimby": result[3]}

        response.append(timetamp_state)

    # Return the response in json format
    return jsonify(response)

# Route to get the quantity of frame rendered for each group
@graphics.route("/graphics/frame-computed")
def frames_computed():
    projects_rendered = execute_from_file("tractor", "frame_computed.sql")
    projects_validated = sessions["harvest"].query(func.count(1), Project.name) \
        .filter(Layer.frame_id == Frame.id) \
        .filter(Frame.shot_id == Shot.id) \
        .filter(Shot.sequence_id == Sequence.id) \
        .filter(Sequence.project_id == Project.id) \
        .filter(Layer.valid == True) \
        .group_by(Project.name)

    # Initialize the final response
    response = [{"project": project["name"], "rendered": int(0), "valid": int(0)} for project in get_projects_infos()]
    response.remove({"project": "TEST_PIPE", "rendered": int(0), "valid": int(0)})

    # Loop over all the rows of the sql response
    for project_rendered in projects_rendered:
        for project in response:
            if project_rendered[0] == project["project"]:
                project["rendered"] = project_rendered[1]
    for project_validated in projects_validated:
        for project in response:
            if project_validated[1] in project["project"]:
                project["valid"] = project_validated[0]

    # Return the response in json format
    return jsonify(response)
