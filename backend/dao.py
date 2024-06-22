from db import *
from sqlalchemy.orm import scoped_session
from datetime import datetime

# 유저 검색에 필요한 Key가 잘못된 경우 Raise
class InvalidateUserQuery(Exception):
    def __init__(self, msg:str=None):
        self.msg = "This function require 1 parameter at least." if msg != None else msg
    
    def __str__(self):
        return self.msg
    
class UserDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def insert_user(self, name:str, email:str, hashed_password:str):
        u = User(name, email, hashed_password)
        self.db_session.add(u)
        self.db_session.commit()
    
    def insert_authcode(self, authcode:int, name:str):
        a = Authcode(authcode, name)
        self.db_session.add(a)
        self.db_session.commit()

    def get_authcode(self, authcode:int) -> Authcode:
        return self.db_session.query(Authcode).filter_by(authcode=authcode).one_or_none()
    
    def delete_authcode(self, authcode:int):
        self.db_session.query(Authcode).filter_by(authcode=authcode).delete()
        self.db_session.commit()
    
    def get_user(self, uid:int=None, email:str=None) -> User:
        if uid == None or email == None:
            raise InvalidateUserQuery()
        elif uid != None:
            return self.db_session.query(User).filter_by(uid=uid).one_or_none()
        elif email != None: 
            return self.db_session.query(User).filter_by(email=email).one_or_none()
    
    def update_pwd(self, uid:int, hashed_pwd:str):
        self.db_session.query(User).filter_by(uid=uid).update({
            "pwd":hashed_pwd
        })
        self.db_session.commit()

    def delete_user(self, uid:int):
        self.db_session.query(User).filter_by(uid=uid).delete()
        self.db_session.commit()

class MemberDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def insert_member(self, name:str, active_duty:str, stdid:int, major:str, contact:str):
        m = Member(name, active_duty, stdid, major, contact)
        self.db_session.add(m)
        self.db_session.commit()

    def get_all_memebers(self) -> list:
        return self.db_session.query(Member).all()
    
    def delete_member(self, id:int):
        self.db_session.query(Member).filter_by(id=id).delete()
        self.db_session.commit()

class DutyDao:
    pass

class DutyLogDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session
    
    def insert_dutyLog(self, uid:int, duty_type:int, date:str):
        l = DutyLog(uid, duty_type, datetime.strftime(date, "%Y%m%d"))
        self.db_session.add(l)
        self.db_session.commit()

    def get_all_dutyLog(self) -> list:
        return self.db_session.query(DutyLog).all()

    def get_dutyLogByUid(self, uid:int) -> list:
        return self.db_session.query(DutyLog).filter_by(uid=uid).all()
    
    def get_dutyLogByDate(self, date:str) -> list:
        date = datetime.strftime(date, "%Y%m%d") # Format must be YYYYMMDD
        return self.db_session.query(DutyLog).filter_by(date=date).all()
    
    def delete_dutyLog(self, id:int):
        self.db_session.query(DutyLog).filter_by(id=id).delete()
        self.db_session.commit()

class ScoreTableDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def insert_subject(self, title:str, score:int):
        s = Score(title, score)
        self.db_session.add(s)
        self.db_session.commit()

    def delete_subject(self, id:int):
        self.db_session.query(Score).filter_by(id=id).delete()
        self.db_session.commit()

    def get_all_subject(self) -> list:
        return self.db_session.query(Score).all()