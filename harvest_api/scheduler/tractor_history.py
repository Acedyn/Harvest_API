import atexit, datetime

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job
from mappings.harvest_tables import HistoryFarm, HistoryProject, HistoryBlade
from routes.stats import get_farm_status, get_projects_usage, get_blades_usage
from routes.infos import get_projects_infos

# Buffer to store the result of every query, and flush every hour when we store its content in postgresql
class HistoryBuffer():
    def __init__(self):
        self.farm_usage = {"busy": int(0), "free": int(0), "nimby": int(0), "off": int(0)}
        self.projects_usage = {project["name"]: int(0) for project in get_projects_infos()}
        self.blades_usage = {}
        self.farm_counter = int(0)
        self.projects_counter = int(0)
        self.blades_counter = int(0)

    def __str__(self):
        return f"Buffer : \nbusy: {self.farm_usage['busy']}, free: {self.farm_usage['free']}, nimby: {self.farm_usage['nimby']}, off: {self.farm_usage['off']}, counter: {self.farm_counter}\nprojects: {self.projects_usage}, counter: {self.projects_counter}\nblades: {self.blades_usage}, counter: {self.blades_counter}"

history_buffer = HistoryBuffer()

# Store the current state of the blades in a new record in the history table
def update_farm_history(history_buffer: HistoryBuffer):
    # Get the working blades
    blades_free, blades_busy, blades_nimby, blades_off = get_farm_status()
    # Store the result of the query in the buffers
    history_buffer.farm_usage["busy"] += int(blades_busy)
    history_buffer.farm_usage["free"] += int(blades_free)
    history_buffer.farm_usage["nimby"] += int(blades_nimby)
    history_buffer.farm_usage["off"] += int(blades_off)
    # Increase the counter so we can compute the average
    history_buffer.farm_counter += 1

def update_projects_history(history_buffer: HistoryBuffer):
    # Get the project usage on the farm
    projects_usage = get_projects_usage()
    for project_usage in projects_usage:
        # Check if the project exist in the database
        if project_usage["name"] in history_buffer.projects_usage:
            history_buffer.projects_usage[project_usage["name"]] += project_usage["value"]
    # Increase the counter so we can compute the average
    history_buffer.projects_counter += 1

def update_blades_history(history_buffer: HistoryBuffer):
    # Get the blade usage on the farm
    blades_usage = get_blades_usage()
    for blade_usage in blades_usage:
        # Check if the blade exist in the buffer
        if blade_usage["name"] in history_buffer.blades_usage:
            history_buffer.blades_usage[blade_usage["name"]] += blade_usage["value"]
        else:
            history_buffer.blades_usage[blade_usage["name"]] = blade_usage["value"]
    # Increase the counter so we can compute the average
    history_buffer.blades_counter += 1

def update_history_database(history_buffer: HistoryBuffer):
    record_time = datetime.datetime.now()
    # Add the result to a new record in the history table
    history_record = HistoryFarm(date = record_time, 
        blade_busy = int(history_buffer.farm_usage["busy"] / history_buffer.farm_counter), 
        blade_free = int(history_buffer.farm_usage["free"] / history_buffer.farm_counter), 
        blade_nimby = int(history_buffer.farm_usage["nimby"] / history_buffer.farm_counter), 
        blade_off = int(history_buffer.farm_usage["off"] / history_buffer.farm_counter))
    sessions["harvest"].add(history_record)
    sessions["harvest"].commit()
    # Add the result to a new record in the history_project table
    for project_name, project_usage in history_buffer.projects_usage.items():
        project_history_record = HistoryProject(date = record_time,
            project_id = [project["id"] for project in get_projects_infos() if project["name"] == project_name][0],
            blade_busy = int(project_usage / history_buffer.projects_counter))
        sessions["harvest"].add(project_history_record)
    sessions["harvest"].commit()
    # Add the result to a new record in the history_blades table
    for blade_name, blade_usage in history_buffer.blades_usage.items():
        blade_history_record = HistoryBlade(date = record_time,
            blade = blade_name,
            computetime = datetime.time(minute = blade_usage))
        sessions["harvest"].add(blade_history_record)
    sessions["harvest"].commit()
    # Reset the buffer
    history_buffer.__init__()

# Initialize the scheduler with the update_tractor_history function
tractor_history_updater = BackgroundScheduler()
# Trigger the functions every 2 minutes
tractor_history_updater.add_job(func = lambda: update_farm_history(history_buffer), trigger = "interval", seconds = 2, id = "tractor_history")
tractor_history_updater.add_job(func = lambda: update_projects_history(history_buffer), trigger = "interval", seconds = 2, id = "projects_history")
tractor_history_updater.add_job(func = lambda: update_blades_history(history_buffer), trigger = "interval", seconds = 2, id = "blades_history")
tractor_history_updater.add_job(func = lambda: update_history_database(history_buffer), trigger = "interval", seconds = 6, id = "database_history")

# Shut down the scheduler when exiting the app
atexit.register(lambda: tractor_history_updater.shutdown())
