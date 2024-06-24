import jwt
from service import *
from functools import wraps
from flask_cors import CORS
from config import JWT_SECRET_KEY
from db import init_database, db_session
from flask import Flask, request, g, Response

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.cookies.get("authorization")

        if token is None:
            return Response(status = 400)
        else:
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, 'HS256')
            except Exception:
                return Response(response="Invalid Token", staus=401)
            
            g.uid = payload['uid']
            g.name = payload['name']
            g.email = payload['email']

        return f(*args, **kwargs)
    return wrapper

app = Flask(__name__)
CORS(app)

dao = {
    'user':UserDao(db_session),
    'member':MemberDao(db_session),
    'dutyLog':DutyLogDao(db_session),
    'scoreTable':ScoreTableDao(db_session)
}

userService = UserService(dao['user'])
memberService = MemberService(dao['member'])
dutyLogService = DutyLogService(dao['dutyLog'])
scoreService = ScoreService(dao['scoreTable'])

#
# 로봇 생성 코드 추기
#

# User Endpoints
@app.route("/registration", methods=["POST"])
def registration() -> Response:
    payload = request.get_json()

    try:
        email = payload['email']
        pwd = payload['pwd']
        pwd_chk = payload['pwd_chk']
        authcode = int(payload['authcode'])
    except KeyError:
        return Response(status=400)
    
    print(pwd)

    if pwd != pwd_chk:
        return Response(response="패스워드를 다시 확인해 주세요.", status=400)
    
    return userService.registration(email, pwd, authcode)

@app.route("/authenticate", methods=["POST"])
def authenticate() -> Response:
    payload = request.get_json()

    try:
        email = payload['email']
        pwd = payload['pwd']
    except KeyError:
        return Response(status=400)
    
    print(pwd)
    
    return userService.authenticate(email, pwd)

@app.route("/update-password", methods=["POST"])
@login_required
def update_password() -> Response:
    payload = request.get_json()

    try:
        old_pwd = payload['old_pwd']
        new_pwd = payload['new_pwd']
        new_pwd_chk = payload['new_pwd_chk']
    except KeyError:
        return Response(status=400)
    
    if new_pwd != new_pwd_chk:
        return Response(response="패스워드를 다시 확인해 주세요.", status=400)
    
    return userService.update_password(old_pwd, new_pwd)

@app.route("/withdraw", methods=["POST"])
@login_required
def withdraw() -> Response:
    payload = request.get_json()

    try:
        pwd = payload['pwd']
    except KeyError:
        return Response(status=400)
    
    return userService.delete_self(pwd)

@app.route("/issue-authcode", methods=["POST"])
def issue_authcode() -> Response:
    payload = request.get_json()

    try:
        name = payload['name']
        is_king = bool(payload['is_king'])
    except KeyError:
        return Response(status = 400)
    
    return userService.issue_authcode(name, is_king)

# Member Endpoints

if __name__ == "__main__":
    init_database()
    app.run("127.0.0.1", port=4444, debug=True)