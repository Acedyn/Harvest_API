from flask import Blueprint, jsonify, request
from sqlalchemy.sql import select
from database import execute_from_file, sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer
import re

########################################
## Validation blueprint : Set of routes that will return and get data
## related to frame validation
########################################

# Initialize the set of routes for validation
validation = Blueprint("validation", __name__)

# Route used to get the project's state of the harvest database
@validation.route("/validation/validated-progression/<project>", methods = ["GET"])
def validated_progression_project(project):
    query = get_project_query(project)
    results = engines["harvest"].execute(query)

    for result in results:
        print(result)
    

    return "Hello world"


# Route used to get the sequence's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>", methods = ["GET"])
def validated_progression_sequence(project):


    return "Hello world"


# Route used to get the shot's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>", methods = ["GET"])
def validated_progression_shot(project):


    return "Hello world"

# Route used to get the frame's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>/<frame>", methods = ["GET"])
def validated_progression_frame(project):


    return "Hello world"



# Route used to update the project's state of the harvest database
@validation.route("/validation/validate-progression/<project>", methods = ["POST"])
def validate_progression_project(project):
    data = request.json

    return jsonify(data)


# Route used to update the sequence's state of the harvest database
@validation.route("/validation/validate-progression/<project>/<sequence>", methods = ["POST"])
def validate_progression_sequence(project):
    data = request.json

    return jsonify(data)


# Route used to update the shot's state of the harvest database
@validation.route("/validation/validate-progression/<project>/<sequence>/<shot>", methods = ["POST"])
def validate_progression_shot(project):
    data = request.json

    return jsonify(data)


# Route used to update the frame's state of the harvest database
@validation.route("/validation/validate-progression/<project>/<sequence>/<shot>/<frame>", methods = ["POST"])
def validate_progression_frame(project):
    data = request.json

    return jsonify(data)



# Route used to get all the frames that has been rendered on the farm since the last validation
@validation.route("/validation/unvalidated-progression/<project>", methods = ["GET"])
def unvalidated_progression(project):
    # Query the last validation date of the given parameter
    last_validation = sessions["harvest"].query(Project.last_validation).filter(Project.name == project.upper()).first()

    # Set the parameters from the project name and the last validation date
    parameters = ({"project": project.upper(), "last_validation": last_validation[0].strftime("%Y-%m-%d %H:%M:%S")})
    # Query from the unvalidated_frames.sql file, with the parameters
    results = execute_from_file("tractor", "unvalidated_frames.sql", parameters)

    # Initialize the final response that will contain all the frames
    response = []

    # Loop over all the result to store them in the response
    for result in results:
        # Cast the result to the right type
        sequence = int(re.sub("[^0-9]", '', result["sequence"]))
        shot = int(re.sub("[^0-9]", '', result["shot"]))
        # Append the casted result
        response.append({"sequence": sequence, "shot": shot, "frame": result["frame"]})

    return jsonify(response)


########################################
# Utility functions
########################################

def get_project_query(name: str):
    project_query = select([Project.name, Project.id]).where(Project.name == name.upper())
    project_query_alias = project_query.alias()
    sequence_query = select([Sequence.index, Sequence.id]).where(Sequence.project_id == project_query_alias.c.id)

    return sequence_query

