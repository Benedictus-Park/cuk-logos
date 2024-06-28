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
        token = request.headers.get("Authorization")

        if token is None:
            return Response("Invalid Token", 401)
        else:
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, 'HS256')
            except Exception:
                return Response("Invalid Token", 401)
            
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
    'scoreTable':ScoreTableDao(db_session),
    'duty':DutyDao(db_session)
}

userService = UserService(dao['user'])
memberService = MemberService(dao['member'])
scoreService = ScoreService(dao['scoreTable'])
dutyService = DutyService(dao['duty'])

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
    
    return userService.authenticate(email, pwd)

@app.route("/retrive-pwd-req", methods=["POST"])
def retrive_pwd_req() -> Response:
    payload = request.get_json()

    try:
        email = payload['email']
    except KeyError:
        return Response(status=400)
    
    return userService.retrive_pwd_req(email)

@app.route("/reset-pwd", methods=["POST"])
def reset_pwd() -> Response:
    payload = request.get_json()

    try:
        pwd = payload['pwd']
        pwd_chk = payload['pwd_chk']
        key = payload['key']
    except KeyError:
        return Response(status=400)
    
    if pwd != pwd_chk:
        return Response("패스워드를 다시 확인하세요.", 400)
    
    return userService.reset_pwd(pwd, key)

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
@login_required
def issue_authcode() -> Response:
    payload = request.get_json()

    try:
        name = payload['name']
    except KeyError:
        return Response(status = 400)
    
    return userService.issue_authcode(name)

# Member Endpoints
@app.route("/sync-members", methods=["POST"])
@login_required
def sync_members() -> Response:
    return memberService.sync_members()

@app.route("/get-all-members", methods=["POST"])
@login_required
def get_all_members() -> Response:
    return memberService.get_members()

# Scoretable Endpoints
@app.route("/sync-scoretable", methods=["POST"])
@login_required
def sync_scoretable() -> Response:
    return scoreService.sync_subjects()

@app.route("/get-scoretable", methods=["POST"])
@login_required
def get_scoretable() -> Response:
    return scoreService.get_subjects()

# Duty Endpoints
@app.route("/fill-gspread-date", methods=["POST"])
@login_required
def fill_gspread_date() -> Response:
    payload = request.get_json()

    try:
        month_plus = payload['month_plus']
    except KeyError:
        return Response(status=400)
    
    return dutyService.fill_gsheet_date(month_plus)

@app.route("/sync-duty", methods=["POST"])
@login_required
def sync_duty() -> Response:
    return dutyService.sync_duty(memberService.dao.get_all_memebers())

if __name__ == "__main__":
    init_database()
    app.run("127.0.0.1", port=4444, debug=True)