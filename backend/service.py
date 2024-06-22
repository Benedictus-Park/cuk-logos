import jwt
import bcrypt
from dao import *
from random import randint
from config import JWT_SECRET_KEY
from flask import jsonify, Response, g
from datetime import datetime, timedelta, timezone

def create_jwt(uid:int, name:str) -> str:
    return jwt.encode({
        'uid':uid,
        'name':name,
        'exp':datetime.now(timezone.utc) + timedelta(hours=1)
        },
        JWT_SECRET_KEY,
        algorithm='HS256'
    )

class UserService:
    def __init__(self, dao:UserDao):
        self.dao = dao

    def registration(self, email:str, pwd:str, authcode:str) -> Response:
        if self.dao.get_user(email=email) != None:
            return Response("이미 사용 중인 이메일입니다.", 409)
        else:
            pwd = bcrypt.hashpw(pwd.encode('utf-8', bcrypt.gensalt()).decode('utf-8'))
            auth = self.dao.get_authcode(authcode)

            if auth == None:
                return Response("인증코드가 틀렸습니다.", 401)

            self.dao.delete_authcode(authcode)
            self.dao.insert_user(auth.name, email, pwd)

            return Response("가입 성공!", 201)
        
    def authenticate(self, email:str, pwd:str) -> Response:
        u = self.dao.get_user(email)

        if u == None:
            return Response("로그인 정보가 틀렸습니다.", 401)
        elif not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("로그인 정보가 틀렸습니다.", 401)
        else:
            json = {
                'name':u.name
            }

            rsp = jsonify(json)
            rsp.set_cookie(key='authorization', value=create_jwt(g.uid, g.name), status = 202)

            return rsp
    
    def update_password(self, pwd:str, new_pwd:str) -> Response:
        u = self.dao.get_user(g.uid)

        if not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("기존 패스워드가 틀렸습니다.", 401)
        else:
            pwd = bcrypt.hashpw(new_pwd.encode('utf-8', bcrypt.gensalt()).decode('utf-8'))
            self.dao.update_pwd(u.uid, pwd)
            return Response(status=200)

    def delete_self(self, pwd:str) -> Response:
        u = self.dao.get_user(g.uid) 

        if not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("패스워드가 틀렸습니다.", 401)
        else:
            self.dao.delete_user(g.uid)
            return Response(status=200)
    
    def issue_authcode(self, name:str) -> Response:
        authcode = randint(100000, 999999)
        self.dao.insert_authcode(authcode, name)

        payload =  {
            "name":name,
            "authcode":authcode
        }

        rsp = jsonify(payload)
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp

class MemberService:
    def __init__(self, dao:MemberDao):
        self.dao = dao

    def regist_member(self, members:list) -> Response:
        for member in members:
            self.dao.insert_member(member)
        
        rsp = Response(status=201)
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp
    
    def get_members(self) -> Response:
        members = self.dao.get_all_memebers()

        rsp = jsonify({
            "members":[] if len(members) == 0 else members
        })
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp
    
    def delete_member(self, id:int) -> Response:
        self.dao.delete_member(id)

        rsp = Response(status=201)
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp
    
class ScoreService:
    def __init__(self, dao:ScoreTableDao):
        self.dao = dao

    def regist_subject(self, title:str, score:int) -> Response:
        self.dao.insert_subject(title, score)
        
        rsp = Response(status=201)
        rsp.set_cookie("authoriztion", create_jwt(g.uid, g.name))

        return rsp
    
    def delete_subject(self, id:int) -> Response:
        self.dao.delete_subject(id)

        rsp = Response(status=200)
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp
    
    def get_subjects(self) -> Response:
        l = self.dao.get_all_subject()

        payload = {
            'subjects':[] if len(l) == 0 else l
        }
        rsp = jsonify(payload)
        rsp.set_cookie("authorization", create_jwt(g.uid, g.name))

        return rsp

class DutyLogService:
    pass
    # Duty 관련은 맨 마지막에 처리
        
# Duty Type
    # 0 - 평일미사
    # 1 - 주일미사
    # 2 - 입학미사
    # 3 - 개강미사
    # 4 - 성목요일
    # 5 - 성금요일
    # 6 - 부활성야
    # 7 - 성모의밤
    # 8 - 세례식
    # 9 - 쨈