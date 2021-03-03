from server import tractor_db

# Currently only the Blade table is used in the tractor_route_stat.py file

# Mapping to get to the job table
class Job(tractor_db.Model):
    __bind_key__ = "tractor"
    __table__ = tractor_db.Model.metadata.tables["job"]

# Mapping to get to the task table
class Task(tractor_db.Model):
    __bind_key__ = "tractor"
    __table__ = tractor_db.Model.metadata.tables["task"]

# Mapping to get to the invocation table
class Invocation(tractor_db.Model):
    __bind_key__ = "tractor"
    __table__ = tractor_db.Model.metadata.tables["invocation"]

# Mapping to get to the command table
class Command(tractor_db.Model):
    __bind_key__ = "tractor"
    __table__ = tractor_db.Model.metadata.tables["command"]

# Mapping to get to the blade table
class Blade(tractor_db.Model):
    __bind_key__ = "tractor"
    __table__ = tractor_db.Model.metadata.tables["blade"]
