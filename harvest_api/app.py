from server import create_app
from waitress import serve
from config.config import DevelopmentConfig, ProductionConfig, Config
import sqlalchemy
import getpass, sys, getopt

# Get aguments
argv = sys.argv[1:]
opts, args = getopt.getopt(argv, "e:d:")


# Get password from user
password = getpass.getpass("Database password: ")


# Load config from config.py
config = Config(password)
# If the -e dev argument has been passed use development configuration
if ("-e", "dev") in opts or ("-e", "development") in opts:
    for opt, arg in opts:
        if(opt == "-d"):
            config = DevelopmentConfig(password, arg)
            break
        else:
            config = DevelopmentConfig(password)
# If the -e prod argument has been passed use production configuration
elif ("-e", "prod") in opts or ("-e", "production") in opts:
    for opt, arg in opts:
        if(opt == "-d"):
            config = ProductionConfig(password, arg)
            break
        else:
            config = ProductionConfig(password)
# If the no -e argument has been passed use default configuration
else:
    for opt, arg in opts:
        if(opt == "-d"):
            config = Config(password, arg)
        else:
            config = Config(password)


# Create the flask app from the config file
try:
    app = create_app(config)
except Exception as exception:
    print(exception)
    print ("ERROR: Failed to connect to the database, it can be due to a wrong password, or a wrong adress")
    sys.exit()


# Start the flask application
if __name__ == '__main__':
    if config.environment == "prod":
        # If we are in production serve with waitress
        serve(app, host=config.host, port=config.port)
    elif config.environment == "dev":
        # If we are in development serve with flask
        app.run(debug = True, host=config.host, port=config.port)
    else:
        # By default serve with flask
        app.run(debug = True, host=config.host, port=config.port)
