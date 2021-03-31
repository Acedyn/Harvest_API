import warnings

# These class are used to store all the config infos
# They are imported in app.py to apply the config to the flask app
class Config(object):
    def __init__(self, db_password = "", db_adress = "localhost:5432", db_user = "postgres", app_port = "8080"):
        # Initialize the attributes using the given parameters
        self.app_port = app_port
        self.db_password = db_password
        self.SQLALCHEMY_DATABASES = {
            "tractor": "postgresql://" + db_user + ":" + db_password + "@" + db_adress + "/tractor",
            "harvest": "postgresql://" + db_user + ":" + db_password + "@" + db_adress + "/harvest",
            "nimbygame": "postgresql://" + db_user + ":" + db_password + "@" + db_adress + "/nimbygame",
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
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# To use these config, add "-e dev" when starting the server 
class DevelopmentConfig(Config):
    def __init__(self, db_password = "", db_adress = "localhost:5432", db_user = "postgres", app_port = "8080"):
        Config.__init__(self, db_password, db_adress, db_user, app_port)

    environment = "dev"
    app_host="0.0.0.0"
    # TODO: Fix the scheduler so it does not start another scheduler every time the app reload
    DEBUG = False
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

# To use these config, add "-e prod" when starting the server 
class ProductionConfig(Config):
    def __init__(self, db_password = "", db_adress = "localhost:9876", db_user = "root", app_port = "5000"):
        Config.__init__(self, db_password, db_adress, db_user, app_port)

    environment = "prod"
    app_host="0.0.0.0"
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
