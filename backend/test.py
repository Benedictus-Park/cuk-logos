import gspread
import calendar
from dateutil.relativedelta import *
from datetime import datetime, timedelta, timezone

def remove_splits(txt:str) -> str:
    rtn = ""
    for i in range(len(txt)):
        if txt[i] != ' ' and txt[i] != ',':
            rtn += txt[i]
    return rtn

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
            duty_type = -1
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

            duty_list.append([row_days[j].split('(')[0], duty_type, remove_splits(row_text[j])])

# Duty(Date, Duty_Type, Nickname)
duty_data = {
    "복사":[],
    "해설":[],
    "참관":[],
    "독서":[],
    "1독":[],
    "2독":[]
}

for i in duty_list:
    date = datetime(today.year, today.month, int(i[0])).date()

    if i[1] == -1:
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
        if len(duty_names) == 2 and duty_names != "미정":
            duty_data["복사"].append((date, i[1], duty_names))
        else:
            duty_data["복사"].append((date, i[1], duty_names[:2]))
            duty_data["복사"].append((date, i[1], duty_names[2:]))
    
    # 해설 처리
    duty_names = dutyTexts[1].split(':')
    if len(duty_names) > 1:
        duty_names = duty_names[1]

        if duty_names.find("(") != -1:
            name = duty_names.split("(")[0]
            duty_data["해설"].append((date, i[1], name))

            name = duty_names.split("(")[1][:-1]
            duty_data["참관"].append((date, i[1], name))
        else:
            duty_data["해설"].append((date, i[1], duty_names))

    # 독서 처리
    if '1독' in dutyTexts[2]:
        name = dutyTexts[2].split(':')[1]
        duty_data["1독"].append((date, i[1], name))
        name = dutyTexts[3].split(':')[1]
        duty_data["2독"].append((date, i[1], name))
    else:
        name = dutyTexts[2].split(':')[1]
        duty_data["독서"].append((date, i[1], name))

print(duty_data)