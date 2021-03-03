from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os

# Initialize the engines and session dictionnary
# We initialize it here to avoid circular imports
engines = {}
sessions = {}



# Initialize SQLAlchemy from config
def create_orm(config_file):
    # Create the engines that will connect to the databases
    engines["tractor"] = create_engine(config_file.SQLALCHEMY_DATABASES["tractor"])
    engines["harvest"] = create_engine(config_file.SQLALCHEMY_DATABASES["harvest"])

    # Create the sessions that will be the handle to comunicate with the databaes
    sessions["tractor"] = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engines["tractor"]))
    sessions["harvest"] = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engines["harvest"]))

    # Initialize the SQL functions to make sure we can use them in the raw queries
    execute_from_file("tractor", "func_valid_json.sql")

    return engines, sessions



# Execute an sql query from a file in the queries folder
def execute_from_file(bind, file_name):
    # Get the root path of the queries folder
    query_dir = os.path.join(os.path.dirname(__file__), "queries")

    # Get the file of the coresponding SQL query
    try:
        file = open(os.path.join(query_dir, file_name))
    except Exception as exception:
        print(exception)
        return f"ERROR: Could not open the {file_name} file"
    # Read the content of the file
    query = text(file.read())
    # Execute the query of the file
    try:
        results = engines[bind].execute(query)
    except Exception as exception:
        print(exception)
        return "ERROR: Could not execute the SQL query from {file_name}"

    return results
