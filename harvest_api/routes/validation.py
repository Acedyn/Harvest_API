from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.sql import select, and_, true, false
from database import execute_from_file, sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer
import re

########################################
## Validation blueprint : Set of routes that will return and get data
## related to frame validation
########################################

# Initialize the set of routes for validation
validation = Blueprint("validation", __name__)

# Set of filter that we will use multiple times
combine_filters = (
    Layer.frame_id == Frame.id,
    Frame.shot_id == Shot.id,
    Shot.sequence_id == Sequence.id,
    Sequence.project_id == Project.id,
)

########################################
# GET HARVEST DATA
########################################

# Route used to get the project's state of the harvest database
@validation.route("/validation/validated-progression/<project>", methods = ["GET"])
def validated_progression_project(project):
    # Query all the layers of the given project to get the % of progression
    project_query = select([Sequence.index, func.count(1).label("total"), func.count(1).filter(Layer.valid == true()).label("valid")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        *combine_filters)). \
        group_by(Sequence.index)
    # Execute the query
    results = engines["harvest"].execute(project_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result["total"], "valid": result["valid"]})
    
    return jsonify(response)


# Route used to get the sequence's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>", methods = ["GET"])
def validated_progression_sequence(project, sequence):
    # Query all the layers of the given sequence to get the % of progression
    sequence_query = select([Shot.index, func.count(1).label("total"), func.count(1).filter(Layer.valid == true()).label("valid")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        *combine_filters)). \
        group_by(Shot.index)
    # Execute the query
    results = engines["harvest"].execute(sequence_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result["total"], "valid": result["valid"]})
    
    return jsonify(response)


# Route used to get the shot's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>", methods = ["GET"])
def validated_progression_shot(project, sequence, shot):
    # TODO: Replace the temporary 999999999 from the code
    start = request.args.get('start', default = 0, type = int)
    end = request.args.get('end', default = 999999999, type = int)
    print(start, end)

    # Query all the layers of the given shot to get the % of progression
    shot_query = select([Frame.index, func.count(1).label("total"), func.count(1).filter(Layer.valid == true()).label("valid")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        Shot.index == int(re.sub("[^0-9]", '', shot)), \
        *combine_filters,\
        Frame.index >= start, \
        Frame.index <= end)). \
        group_by(Frame.index)
    # Execute the query
    results = engines["harvest"].execute(shot_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"index": result["index"], "total": result["total"], "valid": result["valid"]})
    
    return jsonify(response)

# Route used to get the frame's state of the harvest database
@validation.route("/validation/validated-progression/<project>/<sequence>/<shot>/<frame>", methods = ["GET"])
def validated_progression_frame(project, sequence, shot, frame):
    # Query all the layers of the given frame to get the % of progression
    frame_query = select([Layer.name, func.count(1).label("total"), func.count(1).filter(Layer.valid == true()).label("valid")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        Sequence.index == int(re.sub("[^0-9]", '', sequence)), \
        Shot.index == int(re.sub("[^0-9]", '', shot)), \
        Frame.index == int(re.sub("[^0-9]", '', frame)), \
        *combine_filters)). \
        group_by(Layer.name)
    # Execute the query
    results = engines["harvest"].execute(frame_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"name": result["name"], "total": result["total"], "valid": result["valid"]})
    
    return jsonify(response)


########################################
# VALIDATE DATA
########################################

# Route used to update the sequence's state of the harvest database
@validation.route("/validation/validate-progression/<project>/sequences", methods = ["POST"])
def validate_progression_sequence(project):
    # Get the json body
    data = request.json

    # Try to query the update of the databse according to the json body
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Sequence.index.in_([layer["sequence"] for layer in data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Make sure your request is a list of object with at least the attribute : sequence in a json format"

    # Return a success message
    return "Tables updated successfully"


# Route used to update the shot's state of the harvest database
@validation.route("/validation/validate-progression/<project>/shots", methods = ["POST"])
def validate_progression_shot(project):
    # Get the json body
    data = request.json

    # Try to query the update of the databse according to the json body
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Shot.index.in_([layer["shot"] for layer in data]))\
        .filter(Sequence.index.in_([layer["sequence"] for layer in data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Make sure your request is a list of object with at least the attributes : sequence, shot in a json format"

    # Return a success message
    return "Tables updated successfully"


# Route used to update the frame's state of the harvest database
@validation.route("/validation/validate-progression/<project>/frames", methods = ["POST"])
def validate_progression_frame(project):
    # Get the json body
    data = request.json

    # Try to query the update of the databse according to the json body
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Frame.index.in_([layer["frame"] for layer in data]))\
        .filter(Shot.index.in_([layer["shot"] for layer in data]))\
        .filter(Sequence.index.in_([layer["sequence"] for layer in data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Make sure your request is a list of object with at least the attributes : sequence, shot, frame in a json format"

    # Return a success message
    return "Tables updated successfully"


# Route used to update the layer's state of the harvest database
@validation.route("/validation/validate-progression/<project>", methods = ["POST"])
def validate_progression_layer(project):
    # Initialize the data holders
    sequence_data = []
    shot_data = []
    frame_data = []
    layer_data = []

    # Parse the json body into the different types of data
    for item in request.json:
        try:
            url = item["url"].split("/")
            url.pop(0)

            new_data = {}
            if(len(url) >= 1):
                new_data["sequence"] = url[0]
            if(len(url) >= 2):
                new_data["shot"] = url[1]
            else:
                sequence_data.append(new_data)
                continue
            if(len(url) >= 3):
                new_data["frame"] = url[2]
            else:
                shot_data.append(new_data)
                continue
            if(len(url) >= 4):
                new_data["layer"] = url[3]
                layer_data.append(new_data)
                continue
            else:
                frame_data.append(new_data)
                continue

        except Exception as exception:
            print(exception)
            return "ERROR: Coult not parse the url attribute of the json body"

    # Try to query the update of the databse according sequence_data
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Sequence.index.in_([item["sequence"] for item in sequence_data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Could not update the given sequence"

    # Try to query the update of the databse according shot_data
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Shot.index.in_([item["shot"] for item in shot_data]))\
        .filter(Sequence.index.in_([item["sequence"] for item in shot_data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Could not update the given shot"

    # Try to query the update of the databse according frame_data
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Frame.index.in_([item["frame"] for item in frame_data]))\
        .filter(Shot.index.in_([item["shot"] for item in frame_data]))\
        .filter(Sequence.index.in_([item["sequence"] for item in frame_data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Could not update the given frames"
    
    # Try to query the update of the databse according layer_data
    try:
        sessions["harvest"].query(Layer.valid)\
        .filter(*combine_filters)\
        .filter(Project.name == re.sub("-", '_', project.upper()))\
        .filter(Layer.name.in_([item["layer"] for item in layer_data]))\
        .filter(Frame.index.in_([item["frame"] for item in layer_data]))\
        .filter(Shot.index.in_([item["shot"] for item in layer_data]))\
        .filter(Sequence.index.in_([item["sequence"] for item in layer_data]))\
        .update({Layer.valid: true()}, synchronize_session = False)

        sessions["harvest"].commit()

    # If an error occured return an error message
    except Exception as exception:
        print(exception)
        return "ERROR: Could not update the given layers"

    # Return a success message
    return "Tables updated successfully"



# Route used to get all the frames that has been rendered on the farm since the last validation
@validation.route("/validation/unvalidated-progression/<project>", methods = ["GET"])
def unvalidated_progression(project):
    # Query the last validation date of the given parameter
    last_validation = sessions["harvest"].query(Project.last_validation).filter(Project.name == re.sub("-", '_', project.upper())).first()

    # Make sure we get the right validation date
    if last_validation is None:
        return "ERROR: Could not found last validation date of given project"

    # Set the parameters from the project name and the last validation date
    parameters = ({"project": re.sub("-", '_', project.upper()), "last_validation": last_validation[0].strftime("%Y-%m-%d %H:%M:%S")})
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

