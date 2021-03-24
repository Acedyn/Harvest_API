import atexit, datetime
from types import SimpleNamespace

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import func

from database import sessions, engines
from mappings.tractor_tables import Blade, BladeUse, Task, Job
from mappings.harvest_tables import History
from routes.stats import blades_status

# Buffer to store the result of every query, and flush every hour when we store its content in postgresql
history_buffer = SimpleNamespace(
    blades_busy = int(0),
    blades_free = int(0),
    blades_nimby = int(0),
    blades_off = int(0),
    project_usage = int(0),
    blades_usage = int(0),
    counter = int(0)
) 

# Store the current state of the blades in a new record in the history table
def update_blades_history(history_buffer: SimpleNamespace):
    # Get the working blades
    blades_busy = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount > 0)
    # Store the result of the query in the buffer
    history_buffer.blades_busy = blades_busy[0][0]
    
    # Get the free blades
    blades_free = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status == "")  \
    .filter(Blade.nimby == "") 
    # Store the result of the query in the buffer
    history_buffer.blades_free = blades_free[0][0]

    # Get the blades with nimby on
    blades_nimby = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) < datetime.timedelta(seconds=180)) \
    .filter(BladeUse.taskcount == 0) \
    .filter(Blade.status.like("%nimby%"))
    # Store the result of the query in the buffer
    history_buffer.blades_nimby = blades_nimby[0][0]

    # Get the blades that are off
    blades_off = sessions["tractor"].query(func.count(1)) \
    .filter(func.upper(Blade.profile).like("MK%")) \
    .filter(Blade.bladeid == BladeUse.bladeid) \
    .filter(BladeUse.taskcount == 0) \
    .filter(func.age(func.current_timestamp(), Blade.heartbeattime) > datetime.timedelta(seconds=180)) \
    # Store the result of the query in the buffer
    history_buffer.blades_off = blades_off[0][0]

    history_buffer.count += 1
    print(history_buffer)
    # Add the result to a new record in the history table
    new_record = History(date = datetime.datetime.now(), blade_busy = blades_busy[0][0], blade_free = blades_free[0][0], blade_nimby = blades_nimby[0][0], blade_off = blades_off[0][0])
    sessions["harvest"].add(new_record)
    sessions["harvest"].commit()


# Initialize the scheduler with the update_tractor_history function
tractor_history_updater = BackgroundScheduler()
# Trigger the function every 1 hours
tractor_history_updater.add_job(func = lambda: update_blades_history(history_buffer), trigger = "interval", minutes = 1, id = "tractor_history")

# Shut down the scheduler when exiting the app
atexit.register(lambda: tractor_history_updater.shutdown())
