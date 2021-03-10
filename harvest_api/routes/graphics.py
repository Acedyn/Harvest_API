from flask import Blueprint, jsonify
from sqlalchemy import func
from sqlalchemy.sql import select, and_, true, false
from database import execute_from_file, sessions, engines
from mappings.harvest_tables import Project, Sequence, Shot, Frame, Layer
import re, datetime

# Initialize the set to routes for tractor
graphics = Blueprint("graphics", __name__)

# Set of filter that we will use multiple times
combine_filters = (
    Layer.frame_id == Frame.id,
    Frame.shot_id == Shot.id,
    Shot.sequence_id == Sequence.id,
    Sequence.project_id == Project.id,
)

# Route for "/crew-progression"
@graphics.route("/graph/progression/<project>")
def crew_progression(project):
    # Query all the layers of the given project to get the project name
    project_query = select([func.date_trunc("day", Layer.validation_date), func.count(1).label("frame_count")]) \
        .where(and_( \
        Project.name == re.sub("-", '_', project.upper()), \
        Layer.valid == true(), \
        Layer.validation_date != None,\
        *combine_filters)). \
        group_by(func.date_trunc("day", Layer.validation_date))
    # Execute the query
    results = engines["harvest"].execute(project_query)

    # Initialize the final response that will contain all the timestamps
    response = []
    # Initialize the count of frame rendered
    frame_count = 0

    # Loop over all the rows of the sql response
    for result in results:
        # Store all the colunm values for the curent row
        date = str(datetime.date(result[0].year, result[0].month, result[0].day))
        timestamp = int(result[0].timestamp()) * 1000
        frame_count += result[1]

        timetamp_state = {"timestamp": timestamp, "date": date, "frame_count": frame_count}

        response.append(timetamp_state)

    # Return the response in json format
    return jsonify(response)
