from flask import Flask
from flask_cors import CORS
from database import sessions, execute_from_file
import os


def create_app(config_file):
    # Initialize the flask app
    app = Flask(__name__)
    # Set the config from the config file
    app.config.from_object(config_file)
    # Add CORS headers to the response
    CORS(app)

    # Register the routes
    from routes.tractor_graphs import tractor_graph
    app.register_blueprint(tractor_graph)
    from routes.tractor_stats import tractor_stat
    app.register_blueprint(tractor_stat)
    from routes.validation import validation
    app.register_blueprint(validation)

    # Make sure we release the resources of the sessions after each requests
    # TODO: Figure out if we realy need to do this and why
    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        sessions["tractor"].remove()
        sessions["harvest"].remove()

    return app
