class Config(object):
    password = ""
    DEBUG = True
    TESTING = True

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + password + "@localhost:5432/tractor"
    SQLALCHEMY_BINDS = {
        "tractor": "postgresql://postgres:" + password + "@localhost:5432/tractor",
        "dev": "postgresql://postgres:" + password + "@localhost:5432/dev"
    }

    def __init__(self, password = ""):
        self.password = password
        self.SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + password + "@localhost:5432/tractor"
        self.SQLALCHEMY_BINDS = {
            "tractor": "postgresql://postgres:" + password + "@localhost:5432/tractor",
            "dev": "postgresql://postgres:" + password + "@localhost:5432/dev"
        }

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
