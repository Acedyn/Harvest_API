from server import tractor_db

# Mapping to get to the job table
class StatsHistory(tractor_db.Model):
    __bind_key__ = "harvest"
    __tablename__ = "StatsHistory"

    time = tractor_db.Column(tractor_db.DateTime, primary_key = True)
    pc_used = tractor_db.Column(tractor_db.Float)
    pc_free = tractor_db.Column(tractor_db.Float)
    pc_nimby = tractor_db.Column(tractor_db.Float)

    def __repr__(self):
        return f"<StatsHistory {self.time}"
