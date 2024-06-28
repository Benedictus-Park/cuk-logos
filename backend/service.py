import jwt
import time
import base64
import bcrypt
import gspread
import calendar
from dao import *
from models import *
from random import randint
from sqlalchemy import text
from mailer import SendMail
from config import JWT_SECRET_KEY
from dateutil.relativedelta import *
from cryptography.fernet import Fernet
from flask import jsonify, Response, g
from datetime import datetime, timedelta, timezone

def remove_splits(txt:str) -> str:
    rtn = ""
    for i in range(len(txt)):
        if txt[i] != ' ' and txt[i] != ',':
            rtn += txt[i]
    return rtn

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

        members = []

        for row in sh:
            name = row[1]
            nickname = row[1][1:] if row[12] == '' else row[12]
            active_duty = "로고스 전례단"
            stdid = -1 if row[2] == '' else row[2]
            major = row[4]
            contact = row[7]

            members.append(Member(name, nickname, active_duty, int(stdid), major, contact))

        self.dao.insert_members(members)

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

        lst_s = []
        sh = sh[2:]
        for i in range(len(sh)):
            sh[i] = sh[i][2:]

        for row in sh:
            lst_s.append(Score(row[0], row[1]))

        self.dao.insert_subjects(lst_s)

        return self.get_subjects()

class DutyService:
    def __init__(self, dao:DutyDao):
        self.dao = dao

    def fill_gsheet_date(self, month_plus:int=0):
        gc = gspread.service_account("catholic-logos-google.json")
        sh = gc.open('전례표-양식').sheet1

        KST = timezone(timedelta(hours=9))

        today = datetime.now(KST) + relativedelta(months=month_plus)
        cal = calendar.Calendar(firstweekday=6)
        month = cal.monthdatescalendar(today.year, today.month)

        for week in range(len(month)):
            for day in range(len(month[week])):
                if month[week][day].month != today.month:
                    month[week][day] = ''
                elif month[week][day].weekday() == 5:
                    month[week][day] = ''
                else:
                    if month[week][day].weekday() == 6:
                        month[week][day] = str(month[week][day].day) + "(보편 : )"
                    else:
                        month[week][day] = month[week][day].day

        offset = 3

        if month[0].count('') == 7:
            month = month[1:]

        if month[-1].count('') == 7:
            month = month[:-1]

        sh.update_cell(1, 1, f'{today.year}-{today.month}')

        for week in month:
            sh.update(f'B{offset}:G{offset + 1}', [week[:-1]])
            offset += 2
            sh.update(f'B{offset}:G{offset}', [[''] * 6])

        sh.format("A1:H20", {
            'horizontalAlignment':"CENTER",
            'textFormat':{'bold':True}
        })

        payload = {
            'jwt':create_jwt(g.uid, g.name, g.email)
        }

        return jsonify(payload)
    
    def sync_duty(self, members:list) -> Response:
        self.dao.db_session.execute(text("TRUNCATE duty;"))
        self.dao.db_session.commit()
        
        gc = gspread.service_account("catholic-logos-google.json")
        sh = gc.open('전례표-양식').sheet1

        sh = sh.get_all_values()

        today = datetime.strptime(sh[0][0], "%Y-%m")

        sh = sh[2:]

        duty_list = []

        for i in range(0, len(sh), 2):
            row_days = sh[i]
            row_text = sh[i + 1]

            for j in range(7):
                if row_days[j] == '':
                    continue
                else:
                    duty_type = 0
                    row_days[j] = remove_splits(row_days[j])

                    if "입학" in row_days[j]:
                        duty_type = 3
                    elif "개강" in row_days[j] or "개교" in row_days[j]:
                        duty_type = 4
                    elif "성목" in row_days[j]:
                        duty_type = 5
                    elif "성금" in row_days[j]:
                        duty_type = 6
                    elif "성야" in row_days[j]:
                        duty_type = 7
                    elif "성탄" in row_days[j]:
                        duty_type = 8
                    elif "견진" in row_days[j]:
                        duty_type = 9
                    elif "세례" in row_days[j]:
                        duty_type = 10
                    elif "성모" in row_days[j]:
                        duty_type = 11

                    duty_list.append([remove_splits(row_days[j].split('(')[0]), duty_type, remove_splits(row_text[j])])

        duty_data = []

        for i in duty_list:
            date = datetime(today.year, today.month, int(i[0])).date()

            if i[1] == 0:
                if date.weekday() == 6:
                    i[1] = 2
                else:
                    i[1] = 1

            dutyTexts = i[2].split('\n')

            if len(dutyTexts) <= 1:
                continue
            
            # 복사 처리
            duty_names = dutyTexts[0].split(':')
            if len(duty_names) > 1:
                duty_names = duty_names[1]
                if len(duty_names) == 2:
                    if duty_names != '미정':
                        duty_data.append((date, i[1], duty_names, '복사'))
                else:
                    duty_data.append((date, i[1], duty_names[:2], '복사'))
                    duty_data.append((date, i[1], duty_names[2:], '복사'))
            
            # 해설 처리
            duty_names = dutyTexts[1].split(':')
            if len(duty_names) > 1:
                duty_names = duty_names[1]

                if duty_names.find("(") != -1:
                    name = duty_names.split("(")[0]
                    duty_data.append((date, i[1], name, '해설'))

                    name = duty_names.split("(")[1][:-1]
                    duty_data.append((date, i[1], name, '참관'))
                else:
                    duty_data.append((date, i[1], duty_names, '해설'))

            # 독서 처리
            if '1독' in dutyTexts[2]:
                name = dutyTexts[2].split(':')[1]
                duty_data.append((date, i[1], name, '1독'))
                name = dutyTexts[3].split(':')[1]
                duty_data.append((date, i[1], name, '2독'))
            else:
                name = dutyTexts[2].split(':')[1]
                duty_data.append((date, i[1], name, '독서'))
        
        pair = dict() # Key(nickname) : Val(mid)

        for member in members:
            pair[member[2]] = member[0]
        
        duty_in = []

        for i in duty_data:
            duty_in.append(Duty(pair[i[2]], i[0], i[1], i[3]))

        self.dao.insert_duties(duty_in)

        return self.get_duties(members)
    
    def get_duties(self, members:list):
        pair_mem = {
            0:'수행전'
        } # Key(mid) : Val(nickname)

        for member in members:
            pair_mem[member[0]] = member[1]

        pair_daytype = {
            1:"평일미사",
            2:"주일미사",
            3:"입학미사",
            4:"개강/개교기념미사",
            5:"성목요일",
            6:"성금요일",
            7:"성야미사",
            8:"성탄미사",
            9:"견진미사",
            10:"세례미사",
            11:"성모의밤"
        }

        l = self.dao.get_all_duties()
        lst_compressed = []

        for i in range(len(l)):
            l[i][1] = pair_mem[l[i][1]]
            l[i][2] = pair_daytype[l[i][2]]
            l[i][4] = pair_mem[l[i][4]] if l[i][1] != pair_mem[l[i][4]] else "본인 수행"

            lst_compressed.append([l[i][1], l[i][2], l[i][4]])

        payload = {
            'duties':lst_compressed,
            'jwt':create_jwt(g.uid, g.name, g.email)
        }
        rsp = jsonify(payload)

        return rsp