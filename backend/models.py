from db import Base
from datetime import datetime
from datetime import date as _date
from sqlalchemy import Column, Integer, Date, VARCHAR, BOOLEAN

class Authcode(Base):
    __tablename__ = "authcode"

    authcode = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)

    def __init__(self, authcode:int, name:str):
        self.authcode = authcode
        self.name = name

class Duty(Base):
    __tablename__ = "duty"
    did = Column(Integer, autoincrement=True, primary_key=True)
    mid = Column(Integer, nullable=False)
    duty_type = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, mid:int, duty_type:Integer, date:_date):
        self.mid = mid
        self.duty_type = duty_type
        self.date = date

class DutyLog(Base):
    __tablename__ = "duty_log"
    did = Column(Integer, primary_key=True)
    mid = Column(Integer, nullable=False)
    duty_type = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, did:int, mid:int, duty_type:int, date:_date):
        self.did = did
        self.mid = mid
        self.duty_type = duty_type
        self.date = date

class Member(Base):
    __tablename__ = "member"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)
    nickname = Column(VARCHAR(30), nullable=True)
    active_duty = Column(VARCHAR(10), nullable=False)
    stdid = Column(Integer, nullable=False)
    major = Column(VARCHAR(50), nullable=False)
    contact = Column(VARCHAR(14), nullable=False)

    def __init__(self, name:str, nickname:str, active_duty:str, stdid:int, major:str, contact:str):
        self.name = name
        self.nickname = nickname
        self.active_duty = active_duty
        self.stdid = stdid
        self.major = major
        self.contact = contact

class Score(Base):
    __tablename__ = "scoretable"

    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(VARCHAR(100), nullable=False)
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