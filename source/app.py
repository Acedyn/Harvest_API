from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig, ProductionConfig
import getpass, sys, getopt

password = getpass.getpass("Password: ")

config = DevelopmentConfig(password)
if environment == "prod":
    config = ProductionConfig(password)
elif environment == "dev":
    config = DevelopmentConfig(password)

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy()
db.reflect(bind="tractor")

