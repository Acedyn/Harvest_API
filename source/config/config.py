import warnings

# These class are used to store all the config infos
# They are imported in app.py to apply the config to the flask app
class Config(object):
    def __init__(self, db_password = "", db_adress = "localhost:5432"):
        self.db_password = db_password
        self.SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + db_password + "@" + db_adress + "/tractor"
        self.SQLALCHEMY_BINDS = {
            "tractor": "postgresql://postgres:" + db_password + "@" + db_adress + "/tractor",
            "dev": "postgresql://postgres:" + db_password + "@" + db_adress + "/dev"
        }

    environment = "default"
    db_password = ""
    port=8080
    host="0.0.0.0"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# To use these config, add "-e dev" when starting the server 
class DevelopmentConfig(Config):
    def __init__(self, db_password = "", db_adress = "localhost:5432"):
        Config.__init__(self, db_password, db_adress)

    environment = "dev"
    port=8080
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    

# To use these config, add "-e prod" when starting the server 
class ProductionConfig(Config):
    def __init__(self, db_password = "", db_adress = "localhost:5432"):
        Config.__init__(self, db_password, db_adress)
        warnings.simplefilter("ignore")

    environment = "prod"
    port=5000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
