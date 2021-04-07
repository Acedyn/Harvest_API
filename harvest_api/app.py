from config.config import DevelopmentConfig, ProductionConfig, ContainerConfig, Config
import getpass, sys, getopt
from server import create_app
from database import create_orm
from waitress import serve

# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:h:u:p:")


# Get the input arguments and store them in a list
config_arg = {}

for opt, arg in opts:
    # Get the host adress of the tractor database
    if(opt == "-th" or opt == "--tractor-host"):
        config_arg["tractor_db_adress"] = arg
    # Get the user of the tractor database
    elif(opt == "-tu" or opt == "--tractor-user"):
        config_arg["tractor_db_user"] = arg
    # Get the name of the tractor database
    elif(opt == "-tn" or opt == "--tractor-name"):
        config_arg["tractor_db_name"] = arg
    # Get the host adress of the harvest database
    if(opt == "-hh" or opt == "--harvest-host"):
        config_arg["harvest_db_adress"] = arg
    # Get the user of the harvest database
    elif(opt == "-hu" or opt == "--harvest-user"):
        config_arg["harvest_db_user"] = arg
    # Get the user of the harvest database
    elif(opt == "-hn" or opt == "--harvest-name"):
        config_arg["harvest_db_name"] = arg
    # Get the port of the flask flask server
    elif(opt == "-p" or opt == "--port"):
        config_arg["app_port"] = arg

# If the -e dev argument has been passed use development configuration
if ("-e", "dev") in opts or ("-e", "development") in opts:
    # Get password from user
    password = getpass.getpass("Database password: ")
    config_arg["tractor_db_password"] = password
    config_arg["harvest_db_password"] = password
    config = DevelopmentConfig(**config_arg)
# If the -e prod argument has been passed use production configuration
elif ("-e", "prod") in opts or ("-e", "production") in opts:
    config = ProductionConfig(**config_arg)
# If the -e docker argument has been passed use docker configuration
elif ("-e", "docker") in opts or ("-e", "container") in opts:
    config = ContainerConfig(**config_arg)
# If the no -e argument has been passed use default configuration
else:
    config_arg["db_password"] = ""
    config = Config(**config_arg)


# Create the orm engines from the config
engines, sessions = create_orm(config)
# Create the flask app from the config
app = create_app(config)


# Start the flask application
if __name__ == '__main__':
    if config.environment == "production":
        # If we are in production serve with waitress
        serve(app, host=config.app_host, port=config.app_port)
    elif config.environment == "development" or config.environment == "container":
        # if we are in development serve with flask
        app.run(debug = config.debug, host=config.app_host, port=config.app_port)
    else:
        pass
        # By default serve with flask
        app.run(debug = config.DEBUG, host=config.app_host, port=config.app_port)
