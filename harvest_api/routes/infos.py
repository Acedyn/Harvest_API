from flask import Blueprint, jsonify
from sqlalchemy import func
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
@infos.route("/infos/projects")
def project_infos():
    # Get all the project, their color and the amount of frames to compute
    projects_query = select([Project.name, Project.color, func.count(1).label("total")]) \
        .where(and_( \
        *combine_filters)). \
        group_by(Project.name, Project.color)
    # Execute the query
    results = engines["harvest"].execute(projects_query)

    # Initialize the final response that will contain project
    response = []
    
    # Convert the sql result to a jsonifyable list
    for result in results:
        response.append({"name": result["name"], "color": result["color"], "frames": result["total"]})
    
    return jsonify(response)
