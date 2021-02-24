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

    return app
