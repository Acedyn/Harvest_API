from flask import Blueprint
from flask import jsonify
from server import tractor_db
from mappings.tractor_tables import Blade

# Initialize the set to routes for tractor
tractor_route_stat = Blueprint("stats", __name__)

# Route for "/pc-work"
@tractor_route_stat.route("/pc-work")
def pc_work():
    PCs_working = Blade.query.filter(Blade.status == "no free slots (1)").filter(Blade.profile != "LAVIT").filter(Blade.profile != "JV").filter(Blade.profile != "windows10").filter(Blade.profile != "TD").filter(Blade.profile != "BUG").filter(Blade.availdisk > 5).count()
    PCs_free = Blade.query.filter(Blade.status == "").filter(Blade.profile != "LAVIT").filter(Blade.profile != "JV").filter(Blade.profile != "windows10").filter(Blade.profile != "TD").filter(Blade.profile != "BUG").filter(Blade.availdisk > 5).count()
    PCs_nimby = Blade.query.filter(Blade.status.startswith("nimby")).filter(Blade.profile != "LAVIT").filter(Blade.profile != "JV").filter(Blade.profile != "windows10").filter(Blade.profile != "TD").filter(Blade.profile != "BUG").filter(Blade.availdisk > 5).count()
    response = [{"name": "Busy", "value": PCs_working}, {"name": "Free", "value": PCs_free}, {"name": "Nimby ON", "value": PCs_nimby}]
    print(response)
    return jsonify(response)

# Route for "/pc-crew"
@tractor_route_stat.route("/pc-crew")
def pc_crew():
    return "hello"
