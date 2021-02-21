from app import tractor_db

class Job(tractor_db.Model):
    __table__ = db.Model.metadata.tables["job"]

class Task(tractor_db.Model):
    __table__ = db.Model.metadata.tables["task"]
