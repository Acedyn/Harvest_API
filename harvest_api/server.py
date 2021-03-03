from flask import Flask
from flask_cors import CORS
from database import sessions, execute_from_file
import os

# Initialize the flask app
# We initialize it here to avoid circular imports
app = Flask(__name__)

def create_app(config_file):
    # Set the config from the config file
    app.config.from_object(config_file)
    # Add CORS headers to the response
    CORS(app)

    # Register the routes
    from routes.tractor_graphs import tractor_graph
    app.register_blueprint(tractor_graph)
    # from routes.tractor_stats import tractor_route_stat
    # app.register_blueprint(tractor_route_stat)

    # Make sure we release the resources of the sessions after each requests
    # TODO: Figure out if we realy need to do this and why
    @app.teardown_appcontext
    def cleanup(resp_or_exc):
        sessions["tractor"].remove()
        sessions["harvest"].remove()

    return app
