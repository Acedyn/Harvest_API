from database import bases

# Currently only the Blade table is used in the tractor_route_stat.py file

# Mapping to get to the job table
class Job(bases["tractor"]):
    __table__ = bases["tractor"].metadata.tables["job"]

# Mapping to get to the task table
class Task(bases["tractor"]):
    __table__ = bases["tractor"].metadata.tables["task"]

# Mapping to get to the invocation table
class Invocation(bases["tractor"]):
    __table__ = bases["tractor"].metadata.tables["invocation"]

# Mapping to get to the command table
class Command(bases["tractor"]):
    __bind_key__ = "tractor"
    __table__ = bases["tractor"].metadata.tables["command"]

# Mapping to get to the blade table
class Blade(bases["tractor"]):
    __bind_key__ = "tractor"
    __table__ = bases["tractor"].metadata.tables["blade"]

# Mapping to get to the bladeuse table
class BladeUse(bases["tractor"]):
    __bind_key__ = "tractor"
    __table__ = bases["tractor"].metadata.tables["bladeuse"]
