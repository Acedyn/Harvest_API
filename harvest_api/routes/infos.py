from flask import Blueprint, jsonify
from sqlalchemy import func, case
from sqlalchemy.sql import select, and_, true, false
from database import sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer

# Initialize the set to routes for infos
infos = Blueprint("infos", __name__)

# Set of filter that we will use multiple times
combine_filters = (
    Layer.frame_id == Frame.id,
    Frame.shot_id == Shot.id,
    Shot.sequence_id == Sequence.id,
    Sequence.project_id == Project.id,
)

# Retrieves the list of the project and multiple infos about them
def get_projects_infos():
    # Get all the project, their color and the amount of frames to compute
    projects_query = select([Project.name, Project.color, func.count(1).label("total"), Project.id]) \
        .where(and_( \
        *combine_filters)). \
        group_by(Project.name, Project.color, Project.id)
    # Execute the query
    results = engines["harvest"].execute(projects_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"name": result["name"], "color": result["color"], "frames": result["total"], "id": result["id"]})
    
    return response

@infos.route("/infos/projects")
def projects_infos():
    # TODO: Find a cleaner way to to this
    # This is to reuse the get_projects_infos function in tractor_history.py
    projects = get_projects_infos()
    return jsonify(projects)

@infos.route("/infos/finished-projects")
def project_finished():
    # Get all the project, their color and the amount of frames to compute
    projects_query = select([Project.name, func.count(1).label("total"), \
        func.count(case([((Layer.valid == True), 1)])).label("valid"), func.max(Layer.validation_date).label("last_validation"), Project.id]) \
        .where(and_( \
        *combine_filters)) \
        .group_by(Project.name, Project.color, Project.id)
    # Execute the query
    results = engines["harvest"].execute(projects_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for index, result in enumerate(results):
        response.append({"name": result["name"], "progression": result["valid"] / result["total"], "id": result["id"], "last_validation": result["last_validation"].timestamp() * 1000})

    return jsonify(sorted(response, key = lambda i: i['last_validation']))
