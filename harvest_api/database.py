from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os

# Initialize the engines, sessions and bases dictionnary
# We initialize it here so we can import them everywhere and avoid circular imports
engines = {}
sessions = {}
bases = {}


# Initialize SQLAlchemy from config
def create_orm(config_file):
    # Create the engines that will connect to the databases
    engines["tractor"] = create_engine(config_file.SQLALCHEMY_DATABASES["tractor"])
    engines["harvest"] = create_engine(config_file.SQLALCHEMY_DATABASES["harvest"])

    # Create the sessions that will be the handle to comunicate with the databaes
    sessions["tractor"] = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engines["tractor"]))
    sessions["harvest"] = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engines["harvest"]))

    # Create the bases that will be the handle for you mappings
    bases["tractor"] = declarative_base()
    bases["harvest"] = declarative_base()

    # Refect all the tables of the tractor's database
    bases["tractor"].metadata.reflect(bind=engines["tractor"])
    from mappings.harvest_tables import Project
    bases["harvest"].metadata.create_all(bind=engines["harvest"])

    # Initialize the SQL functions to make sure we can use them in the raw queries
    execute_from_file("tractor", "func_valid_json.sql")

    return engines, sessions



# Execute an sql query from a file in the queries folder
def execute_from_file(bind, file_name, parameters = ()):
    # Get the root path of the queries folder
    query_dir = os.path.join(os.path.dirname(__file__), "queries")

    # Get the file of the coresponding SQL query
    try:
        with open(os.path.join(query_dir, file_name)) as file:
            # Read the content of the file
            query = text(file.read())
            # Execute the query of the file
            try:
                results = engines[bind].execute(query, parameters)
            except Exception as exception:
                print(exception)
                return f"ERROR: Could not execute the SQL query from {file_name}"
    except Exception as exception:
        print(exception)
        return f"ERROR: Could not open {file_name} to execute sql query"

    return results
