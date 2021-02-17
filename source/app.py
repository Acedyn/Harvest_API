from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig, Config
import getpass, sys, getopt


# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:")

# Get password from user
password = getpass.getpass("Password: ")

# Load config from config.py
config = Config(password)

for opt, arg in opts:
    if arg == "prod" or arg == "production":
        print("Procution config")
        config = ProductionConfig(password)
    elif arg == "dev" or arg == "development":
        print("Development config")
        config = DevelopmentConfig(password)
    else:
        config = Config(password)

# Create the flask app from the config file
app = Flask(__name__)
app.config.from_object(config)

# Create the database interface
db = SQLAlchemy(app)
db.reflect(bind="tractor")

