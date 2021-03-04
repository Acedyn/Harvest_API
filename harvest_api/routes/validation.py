from flask import Blueprint
from flask import jsonify
from database import execute_from_file

########################################
## Validation blueprint : Set of routes that will return and get data
## related to frame validation
########################################

# Initialize the set of routes for validation
validation = Blueprint("validation", __name__)

# Route for "/validation/unvalidated-progression/<project>"
@validation.route("/validation/unvalidated-progression/<project>")
def unvalidated_progression(project):
    # TODO: Get the validation date from the harvest database
    # Set the parameters from the project name and the last validation date
    parameters = ({"project": project, "last_validation": "2021-02-26 20:14:22"})
    # Query from the unvalidated_frames.sql file, with the parameters
    results = execute_from_file("tractor", "unvalidated_frames.sql", parameters)

    for result in results:
        print(result)

    return "OK"