import jwt
import bcrypt
from dao import *
from config import JWT_SECRET_KEY
from flask import jsonify, Response, g
from datetime import datetime, timedelta, timezone

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
                'uid':u.uid,
                'name':u.name
            }

            rsp = jsonify(json)
            rsp.set_cookie(key='authorization', value=jwt.encode({
                        'uid':u.uid,
                        'name':u.name,
                        'exp':datetime.now(timezone.utc) + timedelta(hours=1)
                    },
                    JWT_SECRET_KEY,
                    algorithm='HS256'
                )
            )
            rsp.status = 202

            return rsp
    
    def update_password(self, pwd:str, new_pwd:str):
        u = self.dao.get_user(g.uid)

        if not bcrypt.checkpw(pwd.encode('utf-8'), u.pwd.encode('utf-8')):
            return Response("기존 패스워드가 틀렸습니다.", 401)
        else:
            pwd = bcrypt.hashpw(pwd.encode('utf-8', bcrypt.gensalt()).decode('utf-8'))
            self.dao.update_pwd(u.uid, pwd)
            return Response(status=200)

