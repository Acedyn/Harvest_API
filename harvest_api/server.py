from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

tractor_db = SQLAlchemy()

def create_app(config_file):
    # Create the flask app from the config file
    app = Flask(__name__)
    app.config.from_object(config_file)
    # Add CORS headers to the response
    CORS(app)

    # Create the tractor database interface
    tractor_db.init_app(app)
    with app.app_context():
        tractor_db.reflect(bind="tractor")
        tractor_db.create_all(bind="harvest")

    # Register the routes
    from routes.tractor_graphs import tractor_route_graph
    from routes.tractor_stats import tractor_route_stat
    app.register_blueprint(tractor_route_graph)
    app.register_blueprint(tractor_route_stat)


    return app
