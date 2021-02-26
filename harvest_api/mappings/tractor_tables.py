from server import tractor_db

# These mappings a curently not used, only the .sql files are used for now

# Mapping to get to the job table
class Job(tractor_db.Model):
    __table__ = tractor_db.Model.metadata.tables["job"]

# Mapping to get to the task table
class Task(tractor_db.Model):
    __table__ = tractor_db.Model.metadata.tables["task"]

# Mapping to get to the invocation table
class Invoation(tractor_db.Model):
    __table__ = tractor_db.Model.metadata.tables["invocation"]

# Mapping to get to the command table
class Command(tractor_db.Model):
    __table__ = tractor_db.Model.metadata.tables["command"]

# Mapping to get to the blade table
class Blade(tractor_db.Model):
    __table__ = tractor_db.Model.metadata.tables["blade"]