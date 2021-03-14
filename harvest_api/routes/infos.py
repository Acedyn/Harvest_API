from flask import Blueprint, jsonify
from sqlalchemy import func
from sqlalchemy.sql import select, and_, true, false
from database import sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer

# Initialize the set to routes for tractor
infos = Blueprint("infos", __name__)

# Set of filter that we will use multiple times
combine_filters = (
    Layer.frame_id == Frame.id,
    Frame.shot_id == Shot.id,
    Shot.sequence_id == Sequence.id,
    Sequence.project_id == Project.id,
)

@infos.route("/infos/projects")
def project_infos():
    # Get all the project and the amount of frames to compute
    projects_query = select([Project.name, Project.color, func.count(1).label("total")]) \
        .where(and_( \
        *combine_filters)). \
        group_by(Project.name)
    # Execute the query
    results = engines["harvest"].execute(projects_query)
