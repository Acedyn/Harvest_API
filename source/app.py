from server import create_app
from config import DevelopmentConfig, ProductionConfig, Config
import getpass, sys, getopt

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
app = create_app(config)


# Register the routes
from routes.tractor import tractor_routes
app.register_blueprint(tractor_routes)


# Start the flask application
if __name__ == '__main__':
    if environment == "prod":
        app.run(debug = False, host='0.0.0.0')
    elif environment == "dev":
        app.run(debug = True, host='0.0.0.0')
    else:
        app.run(host='0.0.0.0')
