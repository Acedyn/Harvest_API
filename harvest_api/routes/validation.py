from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.sql import select, and_
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
    # Query all the layers of the given project to get the % of progression
    project_query = select([Sequence.index, func.count(Sequence.index)]).where(and_( \
        Project.name == project.upper(), \
        Sequence.project_id == Project.id, \
        Shot.sequence_id == Sequence.id, \
        Frame.shot_id == Shot.id)). \
        group_by(Sequence.index)
    # Execute the query
    results = engines["harvest"].execute(project_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result[1]})
    
    return jsonify(response)


# Route used to get the sequence's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>", methods = ["GET"])
def validated_progression_sequence(project, sequence):
    # Query all the layers of the given sequence to get the % of progression
    sequence_query = select([Shot.index, func.count(Shot.index)]).where(and_( \
        Project.name == project.upper(), \
        Sequence.project_id == Project.id, \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        Shot.sequence_id == Sequence.id, \
        Frame.shot_id == Shot.id)). \
        group_by(Shot.index)
    # Execute the query
    results = engines["harvest"].execute(sequence_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result[1]})
    
    return jsonify(response)


# Route used to get the shot's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>", methods = ["GET"])
def validated_progression_shot(project, sequence, shot):
    # Query all the layers of the given shot to get the % of progression
    sequence_query = select([Frame.index, func.count(Frame.index)]).where(and_( \
        Project.name == project.upper(), \
        Sequence.project_id == Project.id, \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        Shot.sequence_id == Sequence.id, \
        Shot.index == int(re.sub("[^0-9]", '', shot)), \
        Frame.shot_id == Shot.id)). \
        group_by(Frame.index)
    # Execute the query
    results = engines["harvest"].execute(sequence_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result[1]})
    
    return jsonify(response)

# Route used to get the frame's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>/<frame>", methods = ["GET"])
def validated_progression_frame(project, sequence, shot, frame):
    # Query all the layers of the given frame to get the % of progression
    sequence_query = select([Layer.name, func.count(Layer.name)]).where(and_( \
        Project.name == project.upper(), \
        Sequence.project_id == Project.id, \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        Shot.sequence_id == Sequence.id, \
        Shot.index == int(re.sub("[^0-9]", '', shot)), \
        Frame.shot_id == Shot.id)). \
        Shot.index == int(re.sub("[^0-9]", '', frame)), \
        group_by(Layer.name)
    # Execute the query
    results = engines["harvest"].execute(sequence_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"name": result["name"], "total": result[1]})
    
    return jsonify(response)



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

