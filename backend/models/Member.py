from db import Base
from sqlalchemy import Column, Integer, VARCHAR

class Member:
    __tablename__ = "member"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)
    active_duty = Column(VARCHAR(10), nullable=False)
    stdid = Column(Integer, nullable=False)
    major = Column(VARCHAR(50), nullable=False)
    contact = Column(VARCHAR(14), nullable=False)

    def __init__(self, name:str, active_duty:str, stdid:int, major:str, contact:str):
        self.name = name
        self.active_duty = active_duty
        self.stdid = stdid
        self.major = major
        self.contact = contact