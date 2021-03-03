from flask import Blueprint
from flask import jsonify
from database import execute_from_file
import datetime

# Initialize the set to routes for tractor
tractor_graph = Blueprint("graph", __name__)


# Route for "/crew-progression"
@tractor_graph.route("/crew-progression")
def crew_progression():
    # Query from the crew_progression.sql file
    results = execute_from_file("tractor", "crew_progression.sql")

    # Initialize the timestamp state buffer
    # TODO: Query all the project names from our awesome futur database
    timetamp_state = {
        "date": str(datetime.date(1, 1, 1)),
        "timestamp": 0,
        "DIVE": 0,
        "BARNEY": 0,
        "RELATIVITY": 0,
        "BACKSTAGE": 0,
        "COCORICA": 0,
        "DREAMBLOWER": 0,
        "PIR_HEARTH": 0,
        "HOSTILE": 0,
        "GREEN": 0,
        "FROM_ABOVE": 0,
    }

    # Initialize the final response that will contain all the timestamps
    response = []

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        project = result[0]
        date = str(datetime.date(result[1].year, result[1].month, result[1].day))
        timestamp = int(result[1].timestamp()) * 1000
        done = result[2]

        # If this the timestamp_state is not initialized yet
        if(timetamp_state["timestamp"] == 0):
            # Initialize the timestamp an the date
            timetamp_state["timestamp"] = timestamp
            timetamp_state["date"] = date
        # If we reach a new timestamp
        elif(timetamp_state["timestamp"] != timestamp):
            # Store the curent state of timestamp_state in the response
            response.append(timetamp_state.copy())
            timetamp_state["timestamp"] = timestamp
            timetamp_state["date"] = date

        # Store the value of the row to the current timestamp_state
        timetamp_state[project] = done

    # Append the timestamp_state one last time
    response.append(timetamp_state.copy())

    # Return the response in json format
    return jsonify(response)


# Route for "/frame-computetime"
@tractor_graph.route("/frame-computetime")
def frame_computetime():
    # Query from the frame_computetime.sql file
    results = execute_from_file("tractor", "frame_computetime.sql")

    # Initialize the project stat buffer
    project_stats = {
        "name": ""
    }

    # Initialize the final response that will contain all the project
    response = []

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        computer = result[0]
        project = result[1]
        frametime = round(number = result[2])

        # If this the project_stats is not initialized yet
        if(project_stats["name"] == ""):
            # Initialize the project name
            project_stats["name"] = project
        # If we reach a new project
        elif(project_stats["name"] != project):
            # Store the curent state of project_state in the response
            response.append(project_stats.copy())
            # Reset the buffer for the other project
            project_stats = {
                "name": project
            }

        # Store the value of the row to the current project_stats
        project_stats[computer] = frametime

    # Append the project_state one last time
    response.append(project_stats.copy())

    # Return the response in json format
    return jsonify(response)
