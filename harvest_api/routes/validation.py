from flask import Blueprint, jsonify, request
from database import execute_from_file, sessions
from mappings.harvest_tables import Project
import re

########################################
## Validation blueprint : Set of routes that will return and get data
## related to frame validation
########################################

# Initialize the set of routes for validation
validation = Blueprint("validation", __name__)

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


# Route used to get all the frames that has been rendered on the farm since the last validation
@validation.route("/validation/validate-progression/<project>", methods = ["POST"])
def validate_progression(project):
    data = request.json

    return jsonify(data)