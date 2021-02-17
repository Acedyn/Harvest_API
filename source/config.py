class Config(object):
    password = ""
    DEBUG = False
    TESTING = False

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + password + "@localhost:5432"
    SQLALCHEMY_BINDS = {
        "tractor": "postgresql://postgres:" + password + "@localhost:5432/tractor",
        "dev": "postgresql://postgres:" + password + "@localhost:5432/dev"
    }

    def __init__(self, password = ""):
        self.password = password
        SQLALCHEMY_DATABASE_URI = "postgresql://postgres:" + password + "@localhost:5432"
        SQLALCHEMY_BINDS = {
            "tractor": "postgresql://postgres:" + password + "@localhost:5432/tractor",
            "dev": "postgresql://postgres:" + password + "@localhost:5432/dev"
        }

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
