from flask import Blueprint
from flask import jsonify
from server import tractor_db
from mappings.tractor_tables import Blade, Job, Invocation, Task
from sqlalchemy.sql import text
import os

# Initialize the set to routes for tractor
tractor_route_stat = Blueprint("stats", __name__)

basepath = os.path.dirname(__file__)
query_dir = os.path.join(basepath, "..", "queries")

# Route for "/pc-work"
@tractor_route_stat.route("/pc-work")
def pc_work():
    # Get the working blades
    PCs_working = Blade.query \
    .filter(Blade.status == "no free slots (1)") \
    .filter(Blade.profile != "LAVIT") \
    .filter(Blade.profile != "JV") \
    .filter(Blade.profile != "windows10") \
    .filter(Blade.profile != "TD") \
    .filter(Blade.profile != "BUG") \
    .filter(Blade.availdisk > 5).count()
    # Get the free blades
    PCs_free = Blade.query \
    .filter(Blade.status == "") \
    .filter(Blade.profile != "LAVIT") \
    .filter(Blade.profile != "JV") \
    .filter(Blade.profile != "windows10") \
    .filter(Blade.profile != "TD") \
    .filter(Blade.profile != "BUG") \
    .filter(Blade.availdisk > 5).count()
    # Get the blades with nimby on
    PCs_nimby = Blade.query \
    .filter(Blade.status.startswith("nimby")) \
    .filter(Blade.profile != "LAVIT") \
    .filter(Blade.profile != "JV") \
    .filter(Blade.profile != "windows10") \
    .filter(Blade.profile != "TD") \
    .filter(Blade.profile != "BUG") \
    .filter(Blade.availdisk > 5).count()
    # Return a json
    response = [{"name": "Busy", "value": PCs_working}, {"name": "Free", "value": PCs_free}, {"name": "Nimby ON", "value": PCs_nimby}]
    return jsonify(response)

# Route for "/pc-crew"
@tractor_route_stat.route("/pc-crew")
def pc_crew():
    # Get the file of the coresponding query
    try:
        file = open(os.path.join(query_dir, "blade_crew.sql"))
    except Exception as exception:
        print(exception)
        return "ERROR: Could not open the blade_crew.sql file"
    # Read the content of the file
    query = text(file.read())
    # Execute the query of the file
    try:
        results = tractor_db.engine.execute(query)
    except Exception as exception:
        print(exception)
        return "ERROR: Could not execute the SQL query from blade_crew.sql"

    # Initialize the final response that will contain all the timestamps
    response = []

    # Loop over all the rows of the sql response
    for result in results:
        response.append({result[0]: result[1]})

    # Return the response in json format
    return jsonify(response)
