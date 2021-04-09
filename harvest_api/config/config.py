import warnings

# These class are used to store all the config infos
# They are imported in app.py to apply the config to the flask app
class Config(object):
    def __init__(self, tractor_db_password = "", tractor_db_adress = "localhost:5432", tractor_db_user = "postgres", tractor_db_name = "tractor", \
            harvest_db_password = "", harvest_db_adress = "localhost:5432", harvest_db_user = "postgres", harvest_db_name = "harvest", app_port = "8080"):
        # Initialize the attributes using the given parameters
        self.app_port = app_port
        self.tractor_db_password = tractor_db_password
        self.harvest_db_password = tractor_db_password
        self.SQLALCHEMY_DATABASES = {
            "tractor": "postgresql://" + tractor_db_user + ":" + tractor_db_password + "@" + tractor_db_adress + "/" + tractor_db_name,
            "harvest": "postgresql://" + harvest_db_user + ":" + harvest_db_password + "@" + harvest_db_adress + "/" + harvest_db_name,
        }
        # Ignore the warnings from sqlachemy 
        # (it gives errors because it does not support some types in the tractor's database)
        warnings.filterwarnings("ignore", module="sqlalchemy.dialects.postgresql.base")

    def __repr__(self):
        return f"<{self.__class__.__name__}, env:{self.environment}, port:{self.app_port}>"

    def __str__(self):
        return f"CONFIG Harvest API - {self.environment} \nServing on : {self.app_host}:{self.app_port} \nFrom : {self.SQLALCHEMY_DATABASES}"

    environment = "default"
    app_host="0.0.0.0"
    # TODO: Fix the scheduler so it does not start another scheduler every time the app reload
    debug = False
    testing = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# To use these config, add "-e dev" when starting the server 
class DevelopmentConfig(Config):
    def __init__(self, tractor_db_password = "", tractor_db_adress = "localhost:5432", tractor_db_user = "postgres", tractor_db_name = "tractor", \
            harvest_db_password = "", harvest_db_adress = "localhost:5432", harvest_db_user = "postgres", harvest_db_name = "harvest", app_port = "8080"):
        Config.__init__(self, tractor_db_password, tractor_db_adress, tractor_db_user, tractor_db_name, \
                harvest_db_password, harvest_db_adress, harvest_db_user, harvest_db_name, app_port)

    environment = "development"
    app_host="0.0.0.0"
    # TODO: Fix the scheduler so it does not start another scheduler every time the app reload
    debug = False
    testing = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

# To use these config, add "-e prod" when starting the server 
class ProductionConfig(Config):
    def __init__(self, tractor_db_password = "", tractor_db_adress = "localhost:9876", tractor_db_user = "root", tractor_db_name = "tractor", \
            harvest_db_password = "", harvest_db_adress = "localhost:9876", harvest_db_user = "root", harvest_db_name = "harvest", app_port = "5000"):
        super().__init__(self, tractor_db_password, tractor_db_adress, tractor_db_user, tractor_db_name, \
                harvest_db_password, harvest_db_adress, harvest_db_user, harvest_db_name, app_port)

    environment = "production"
    app_host="0.0.0.0"
    debug = False
    testing = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# To use these config, add "-e docker" when starting the server 
class ContainerConfig(Config):
    def __init__(self, tractor_db_password = "password", tractor_db_adress = "tractor_db:5432", tractor_db_user = "artfx", tractor_db_name = "tractor", \
            harvest_db_password = "password", harvest_db_adress = "harvest_db:5432", harvest_db_user = "artfx", harvest_db_name = "harvest", app_port = "5000"):
        Config.__init__(self, tractor_db_password, tractor_db_adress, tractor_db_user, tractor_db_name, \
                harvest_db_password, harvest_db_adress, harvest_db_user, harvest_db_name, app_port)

    environment = "container"
    app_host="0.0.0.0"
    debug = False
    testing = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
