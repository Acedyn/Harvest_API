from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig, Config
import getpass, sys, getopt

from blueprint import blueprint

# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:")


# Get password from user
password = getpass.getpass("Password: ")


# Load config from config.py
config = Config(password)
environment = "default"
for opt, arg in opts:
    if arg == "prod" or arg == "production":
        print("Procution config")
        environment = "prod"
        config = ProductionConfig(password)
    elif arg == "dev" or arg == "development":
        print("Development config")
        environment = "dev"
        config = DevelopmentConfig(password)
    else:
        config = Config(password)


# Create the flask app from the config file
app = Flask(__name__)
app.config.from_object(config)


# Create the database interface
tractor_db = SQLAlchemy(app)
tractor_db.reflect(bind="tractor")


# Register the routes
app.register_blueprint(blueprint)


# Start the flask application
if __name__ == '__main__':
    if environment == "prod":
        app.run(debug = False)
    elif environment == "dev":
        app.run(debug = True)
    else:
        app.run()
