import atexit, datetime
from types import SimpleNamespace

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job
from mappings.harvest_tables import History
from routes.stats import get_blades_status, get_projects_usage
from routes.infos import get_projects_infos

# Buffer to store the result of every query, and flush every hour when we store its content in postgresql
history_buffer = SimpleNamespace(
    blades_busy = int(0),
    blades_free = int(0),
    blades_nimby = int(0),
    blades_off = int(0),
    project_usage = {project["name"]: int(0) for project in get_projects_infos()},
    blades_usage = {},
    status_counter = int(0),
    project_counter = int(0),
    blades_counter = int(0),
) 

# Store the current state of the blades in a new record in the history table
def update_history(history_buffer: SimpleNamespace):
    # Get the working blades
    blades_free, blades_busy, blades_nimby, blades_off = get_blades_status()
    # Store the result of the query in the buffers
    history_buffer.blades_busy += int(blades_busy)
    history_buffer.blades_free += int(blades_free)
    history_buffer.blades_nimby += int(blades_nimby)
    history_buffer.blades_off += int(blades_off)
    # Increase the counter so we can compute the average
    history_buffer.status_counter += 1

    # Add the result to a new record in the history table
    # new_record = History(date = datetime.datetime.now(), blade_busy = blades_busy, blade_free = blades_free, blade_nimby = blades_nimby, blade_off = blades_off)
    # sessions["harvest"].add(new_record)
    # sessions["harvest"].commit()

def update_projects_history(history_buffer: SimpleNamespace):
    # Get the project usage on the farm
    projects_usage = get_projects_usage()
    for project_usage in projects_usage:
        # Check if the project exist in the database
        if project_usage["name"] in history_buffer.project_usage:
            history_buffer.project_usage[project_usage["name"]] += project_usage["value"]
    # Increase the counter so we can compute the average
    history_buffer.project_counter += 1

def update_blades_history(history_buffer: SimpleNamespace):
    # Get the project usage on the farm
    projects_usage = get_projects_usage()
    for project_usage in projects_usage:
        # Check if the project exist in the database
        if project_usage["name"] in history_buffer.project_usage:
            history_buffer.project_usage[project_usage["name"]] += project_usage["value"]
    # Increase the counter so we can compute the average
    history_buffer.project_counter += 1

# Initialize the scheduler with the update_tractor_history function
tractor_history_updater = BackgroundScheduler()
# Trigger the functions every 2 minutes
tractor_history_updater.add_job(func = lambda: update_history(history_buffer), trigger = "interval", seconds = 5, id = "tractor_history")
tractor_history_updater.add_job(func = lambda: update_projects_history(history_buffer), trigger = "interval", seconds = 5, id = "projects_history")

# Shut down the scheduler when exiting the app
atexit.register(lambda: tractor_history_updater.shutdown())
