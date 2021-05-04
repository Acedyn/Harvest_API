from database import bases
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    DateTime,
    Time,
    String,
    ForeignKey,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

# Mapping to get to the project table
class Project(bases["harvest"]):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    last_validation = Column(DateTime, nullable=False)
    color = Column(String, default="#000000")

    sequence = relationship("Sequence", back_populates="project")

    def __repr__(self):
        return f"<Project {self.id}"

    def __str__(self):
        return f"Project : {self.name}"


# Mapping to get to the sequence table
class Sequence(bases["harvest"]):
    __tablename__ = "sequence"
    __table_args__ = (
        CheckConstraint("index >= 0"),
        UniqueConstraint("index", "project_id", name="unique_sequence"),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    index = Column(Integer, nullable=False)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)

    project = relationship("Project", back_populates="sequence")
    shot = relationship("Shot", back_populates="sequence")

    def __repr__(self):
        return f"<Project {self.id}"

    def __str__(self):
        return f"Sequence : {self.index}"


# Mapping to get to the shot table
class Shot(bases["harvest"]):
    __tablename__ = "shot"
    __table_args__ = (
        CheckConstraint("index >= 0"),
        UniqueConstraint("index", "sequence_id", name="unique_shot"),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    index = Column(Integer, nullable=False)
    sequence_id = Column(Integer, ForeignKey("sequence.id"), nullable=False)

    sequence = relationship("Sequence", back_populates="shot")
    frame = relationship("Frame", back_populates="shot")

    def __repr__(self):
        return f"<Project {self.id}"

    def __str__(self):
        return f"Shot : {self.index}"


# Mapping to get to the frame table
class Frame(bases["harvest"]):
    __tablename__ = "frame"
    __table_args__ = (
        CheckConstraint("index >= 0"),
        UniqueConstraint("index", "shot_id", name="unique_frame"),
    )

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    index = Column(Integer, nullable=False)
    shot_id = Column(Integer, ForeignKey("shot.id"), nullable=False)

    shot = relationship("Shot", back_populates="frame")
    layer = relationship("Layer", back_populates="frame")

    def __repr__(self):
        return f"<Frame {self.id}"

    def __str__(self):
        return f"Frame : {self.index}"


# Mapping to get the layer table
class Layer(bases["harvest"]):
    __tablename__ = "layer"
    __table_args__ = (UniqueConstraint("name", "frame_id", name="unique_layer"),)

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String(50), nullable=False, default="none")
    rendertime = Column(DateTime)
    validation_date = Column(DateTime)
    frame_id = Column(Integer, ForeignKey("frame.id"), nullable=False)
    valid = Column(Boolean, nullable=False, server_default="FALSE")

    frame = relationship("Frame", back_populates="layer")

    def __repr__(self):
        return f"<Layer {self.id}"

    def __str__(self):
        return f"Layer : {self.index}"


# Mapping to get the history table
class HistoryFarm(bases["harvest"]):
    __tablename__ = "history_farm"

    # TODO: Auto fill the date when inserting a row
    date = Column(DateTime, primary_key=True, nullable=False)
    blade_busy = Column(Integer, nullable=False)
    blade_nimby = Column(Integer, nullable=False)
    blade_off = Column(Integer, nullable=False)
    blade_free = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Layer {self.id}"

    def __str__(self):
        return f"Layer : {self.index}"


# Mapping to get the history_project table
class HistoryProject(bases["harvest"]):
    __tablename__ = "history_project"

    date = Column(
        DateTime, ForeignKey("history_farm.date"), primary_key=True, nullable=False
    )
    project_id = Column(
        Integer, ForeignKey("project.id"), primary_key=True, nullable=False
    )
    blade_busy = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<HistoryProject {self.date}"

    def __str__(self):
        return f"HistoryProject : {self.date}, {self.project_id}"


# Mapping to get the history_blades table
class HistoryBlade(bases["harvest"]):
    __tablename__ = "history_blade"

    date = Column(
        DateTime, ForeignKey("history_farm.date"), primary_key=True, nullable=False
    )
    blade = Column(String, primary_key=True, nullable=False)
    computetime = Column(Time, nullable=False)

    def __repr__(self):
        return f"<HistoryProject {self.date}"

    def __str__(self):
        return f"HistoryProject : {self.date}, {self.project_id}"


# Mapping to get the history_compute_time table
class HistoryTotalCompute(bases["harvest"]):
    __tablename__ = "history_total_compute"

    date = Column(DateTime, primary_key=True, nullable=False)
    project_id = Column(
        Integer, ForeignKey("project.id"), primary_key=True, nullable=False
    )
    total_compute = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<HistoryProject {self.date}"

    def __str__(self):
        return f"HistoryProject : {self.date}, {self.project_id}"
