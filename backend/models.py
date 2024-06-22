from db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, Date, VARCHAR

class Authcode(Base):
    __tablename__ = "authcode"

    authcode = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)

    def __init__(self, authcode:int, name:str):
        self.authcode = authcode
        self.name = name

class DutyLog:
    __tablename__ = "duty_log"
    duty_id = Column(Integer, primary_key=True)
    uid = Column(Integer, nullable=False)
    duty_type = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, duty_id:int, uid:int, duty_type:int, date:str):
        self.duty_id = duty_id
        self.uid = uid
        self.duty_type = duty_type
        self.date = datetime.strftime(date, "%Y%m%d") # Format must be YYYYMMDD

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

class Score(Base):
    __tablename__ = "scoretable"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(VARCHAR(12), nullable=False)
    score = Column(Integer, nullable=False)

    def __init__(self, title:str, score:int):
        self.title = title
        self.score = score

class User(Base):
    __tablename__ = "user"

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)
    email = Column(VARCHAR(320), nullable=False, unique=True)
    pwd = Column(VARCHAR(60), nullable=False)

    def __init__(self, name:str, email:str, pwd:str):
        self.name = name
        self.email = email
        self.pwd = pwd