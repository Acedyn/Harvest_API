from flask import Blueprint
from flask import jsonify
from server import tractor_db
from mappings.tractor_tables import Blade

# Initialize the set to routes for tractor
tractor_route_stat = Blueprint("stats", __name__)

# Route for "/pc-used"
@tractor_route_stat.route("/pc_used")
def pc_used():
    return "hello"

# Route for "/pc-free"
@tractor_route_stat.route("/pc-free")
def pc_free():
    return "hello"

# Route for "/pc-nimby"
@tractor_route_stat.route("/pc-nimby")
def pc_nimby():
    return "hello"

# Route for "/pc-crew"
@tractor_route_stat.route("/pc-crew")
def pc_crew():
    return "hello"
