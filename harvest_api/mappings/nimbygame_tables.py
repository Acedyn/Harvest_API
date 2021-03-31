from database import bases
from sqlalchemy import Column, Integer, Boolean, DateTime, Time, String, ForeignKey, CheckConstraint, UniqueConstraint

# Mapping to get to the player table
class Player(bases["nimbygame"]):
    __tablename__ = "player"

    computer = Column(String(50), primary_key = True, nullable=False)
    name = Column(String(50), default = "no name")
    score = Column(Integer, default = 0)

    def __repr__(self):
        return f"<Player {self.computer}"
    
    def __str__(self):
        return f"Player : {self.name}"
