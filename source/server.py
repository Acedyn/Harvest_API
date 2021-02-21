from flask import Flask
from flask_sqlalchemy import SQLAlchemy

tractor_db = SQLAlchemy()

def create_app(config_file):
    # Create the flask app from the config file
    app = Flask(__name__)
    app.config.from_object(config_file)

    # Create the tractor database interface
    tractor_db.init_app(app)
    with app.app_context():
        tractor_db.reflect(bind="tractor")

    return app
