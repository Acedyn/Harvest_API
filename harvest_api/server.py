from flask import Flask
from flask_cors import CORS
import os

basepath = os.path.dirname(__file__)
query_dir = os.path.join(basepath, "queries")

def create_app(config_file):
    # Create the flask app from the config file
    app = Flask(__name__)
    app.config.from_object(config_file)
    # Add CORS headers to the response
    CORS(app)

    # Register the routes
    # from routes.tractor_graphs import tractor_route_graph
    # app.register_blueprint(tractor_route_graph)
    # from routes.tractor_stats import tractor_route_stat
    # app.register_blueprint(tractor_route_stat)

    return app
