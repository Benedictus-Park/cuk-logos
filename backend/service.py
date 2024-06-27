import jwt
import time
import base64
import bcrypt
import gspread
from dao import *
from random import randint
from sqlalchemy import text
from mailer import SendMail
from config import JWT_SECRET_KEY
from cryptography.fernet import Fernet
from flask import jsonify, Response, g
from datetime import datetime, timedelta, timezone

def create_jwt(uid:int, name:str, email:str) -> str:
    return jwt.encode({
        'uid':uid,
        'name':name,
        'email':email,
        'exp':datetime.now(timezone.utc) + timedelta(hours=1)
        },
        JWT_SECRET_KEY,
        algorithm='HS256'
    )

class UserService:
    def __init__(self, dao:UserDao):
        self.dao = dao
        self.encryptor = Fernet(Fernet.generate_key())

    def registration(self, email:str, pwd:str, authcode:str) -> Response:
        if self.dao.get_user(email=email) != None:
            return Response("이미 사용 중인 이메일입니다.", 409)
        else:
            pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            auth = self.dao.get_authcode(authcode)

            if auth == None:
                return Response("인증코드가 틀렸습니다.", 401)

            self.dao.delete_authcode(authcode)
            self.dao.insert_user(auth.name, email, pwd)

            return Response("가입 성공!", 201)
        
    def authenticate(self, email:str, pwd:str) -> Response:
        u = self.dao.get_user(email=email)

        if u == None:
            return Response("로그인 정보가 틀렸습니다.", 401)
        elif not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("로그인 정보가 틀렸습니다.", 401)
        else:
            json = {
                'name':u.name,
                'jwt':create_jwt(u.uid, u.name, u.email)
            }
            rsp = jsonify(json)
            rsp.status_code = 202

            return rsp
        
    def retrive_pwd_req(self, email:str) -> Response:
        u = self.dao.get_user(email=email)

        if u == None:
            return Response("그런 유저 없는데용...?", 404)
        else:
            keybytes = self.encryptor.encrypt((str(u.uid) + "|exp|" + str(time.time())).encode('utf-8'))
            key = base64.b64encode(keybytes).decode('ascii')
                                         
            SendMail(
                "패스워드 재설정 이메일",
                "아래 링크에서 패스워드를 재설정할 수 있습니다.\r\n\r\nhttp://127.0.0.1:5500/frontend/reset-pwd.html?key=" + key,
                u.email
            )
            return Response(200)
        
    def reset_pwd(self, pwd:str, key:str) -> Response:
        encrypted = base64.b64decode(key).decode('ascii')
        decrypted = self.encryptor.decrypt(encrypted.encode('utf-8')).decode('utf-8').split("|exp|")

        if len(decrypted) == 1:
            return Response("잘못된 요청", 400)

        uid = int(decrypted[0])
        created = datetime.fromtimestamp(float(decrypted[1]))

        if created + timedelta(hours=24) < datetime.fromtimestamp(time.time()):
            return Response("만료된 링크입니다.", 403)

        pwd = bcrypt.hashpw(pwd.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        self.dao.update_pwd(uid, pwd)

        return Response(status=200)
    
    def update_password(self, pwd:str, new_pwd:str) -> Response:
        u = self.dao.get_user(g.uid)

        if not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("기존 패스워드가 틀렸습니다.", 401)
        else:
            pwd = bcrypt.hashpw(new_pwd.encode('utf-8', bcrypt.gensalt())).decode('utf-8')
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
        while True:
            authcode = randint(100000, 999999)
            if self.dao.insert_authcode(authcode, name):
                break

        payload =  {
            "name":name,
            "authcode":authcode,
            "jwt":create_jwt(g.uid, g.name, g.email)
        }
        rsp = jsonify(payload)
        rsp.status_code = 201

        return rsp

class MemberService:
    def __init__(self, dao:MemberDao):
        self.dao = dao
    
    def get_members(self) -> Response:
        members = self.dao.get_all_memebers()

        rsp = jsonify({
            "members":[] if len(members) == 0 else members,
            "jwt":create_jwt(g.uid, g.name, g.email)
        })
        rsp.status_code = 202

        return rsp
    
    def sync_members(self) -> Response:
        # 24시간에 한 번 수행되도록!!!
        self.dao.db_session.execute(text("TRUNCATE member;"))
        self.dao.db_session.commit()

        gc = gspread.service_account(filename="catholic-logos-google.json")
        sh = gc.open("로고스 단원 명부").sheet1.get_all_values()

        sh = sh[2:]
        for i in range(len(sh)):
            sh[i] = sh[i][1:]

        for row in sh:
            name = row[1]
            nickname = None if row[12] == '' else row[12]
            active_duty = "로고스 전례단"
            stdid = -1 if row[2] == '' else row[2]
            major = row[4]
            contact = row[7]

            self.dao.insert_member(name, nickname, active_duty, int(stdid), major, contact)

        return self.get_members()
    
class ScoreService:
    def __init__(self, dao:ScoreTableDao):
        self.dao = dao
    
    def get_subjects(self) -> Response:
        l = self.dao.get_all_subject()

        payload = {
            'subjects':[] if len(l) == 0 else l,
            'jwt':create_jwt(g.uid, g.name, g.email)
        }
        rsp = jsonify(payload)

        return rsp
    
    def sync_subjects(self):
        self.dao.db_session.execute(text("TRUNCATE scoretable;"))
        self.dao.db_session.commit()

        gc = gspread.service_account(filename="catholic-logos-google.json")
        sh = gc.open("점수기준표").sheet1.get_all_values()

        sh = sh[2:]
        for i in range(len(sh)):
            sh[i] = sh[i][2:]

        for row in sh:
            title = row[0]
            score = row[1]

            self.dao.insert_subject(title, score)

        return self.get_subjects()

class DutyLogService:
    def __init__(self, dao:DutyLogDao):
        self.dao = dao
    # Duty 관련은 맨 마지막에 처리
        
# Duty Type
    # -1 쨈
    # 1 평일미사
    # 2 주일미사
    # 3 입학미사
    # 4 개강, 개교기념미사
    # 5 성목요일
    # 6 성금요일
    # 7 성야미사
    # 8 성탄미사
    # 9 견진미사
    # 10 세례미사
    # 11 성모의밤