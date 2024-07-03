from db import *
from models import *
from datetime import datetime
from datetime import date as _date
from sqlalchemy.orm import scoped_session

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
    
    def insert_authcode(self, authcode:int, name:str) -> bool:
        a = self.db_session.query(Authcode).filter_by(authcode=authcode).one_or_none()

        if a != None:
            return False

        a = Authcode(authcode, name)
        self.db_session.add(a)
        self.db_session.commit()

        return True

    def get_authcode(self, authcode:int) -> Authcode:
        return self.db_session.query(Authcode).filter_by(authcode=authcode).one_or_none()
    
    def delete_authcode(self, authcode:int):
        self.db_session.query(Authcode).filter_by(authcode=authcode).delete()
        self.db_session.commit()
    
    def get_user(self, uid:int=None, email:str=None) -> User:
        if uid == None and email == None:
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

    def insert_members(self, members:list[Member]):
        self.db_session.add_all(members)
        self.db_session.commit()

    def get_all_memebers(self) -> list[Member]:
        rtn = []

        for i in self.db_session.query(Member).all():
            rtn.append([i])

        return rtn
    
    def delete_member(self, id:int):
        self.db_session.query(Member).filter_by(id=id).delete()
        self.db_session.commit()

class ScoreTableDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def insert_subjects(self, subjects:list[Score]):
        self.db_session.add_all(subjects)
        self.db_session.commit()

    def get_all_subject(self) -> list[Score]:
        rtn = []

        for i in self.db_session.query(Score).all():
            rtn.append([i])

        return rtn
    
class DutyDao:
    def __init__(self, db_session:scoped_session):
        self.db_session = db_session

    def insert_duties(self, duties:list[Duty]):
        self.db_session.add_all(duties)
        self.db_session.commit()

    def get_all_duties(self) -> list[Duty]:
        rtn = []
        
        for i in sorted(self.db_session.query(Duty).all(), key=lambda x:x.date):
            rtn.append([i])

        return rtn
    
    def get_daily_duty(self, date:_date) -> list[Duty]:
        self.db_session.query(Duty).filter_by()