from ..db import Base
from sqlalchemy import Column, Integer, VARCHAR

class Score(Base):
    __tablename__ = "scoretable"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(VARCHAR(12), nullable=False)
    score = Column(Integer, nullable=False)

    def __init__(self, title:str, score:int):
        self.title = title
        self.score = score