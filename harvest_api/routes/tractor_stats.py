from flask import Blueprint
from flask import jsonify
from server import tractor_db
from mappings.tractor_tables import Blade

# Initialize the set to routes for tractor
tractor_route_stat = Blueprint("stats", __name__)

# Route for "/pc-work"
@tractor_route_stat.route("/pc-work")
def pc_work():
    PCs_working = Blade.query.filter_by(status = "no free slots (1)").count()
    response = {"PC_used": PCs_working}
    return jsonify(response)

# Route for "/pc-free"
@tractor_route_stat.route("/pc-free")
def pc_free():
    PCs_free = Blade.query.filter_by(status = "").count()
    response = {"PC_free": PCs_free}
    return jsonify(response)

# Route for "/pc-nimby"
@tractor_route_stat.route("/pc-nimby")
def pc_nimby():
    PCs_nimby = Blade.query.filter(Blade.status.startswith("nimby")).count()
    response = {"PC_nimby": PCs_nimby}
    return jsonify(response)

# Route for "/pc-crew"
@tractor_route_stat.route("/pc-crew")
def pc_crew():
    return "hello"
