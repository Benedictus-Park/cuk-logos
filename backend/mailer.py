from smtplib import SMTP_SSL
from threading import Thread
from email.mime.text import MIMEText
from config import SMTP_EMAIL, SMTP_PWD

def SendMail(title:str, context:str, to:str):
    tr = Thread(target=_SendMail, args=(title, context, to))
    tr.start()

def _SendMail(title:str, context:str, to:str):
    conn = SMTP_SSL("smtp.daum.net:465")
    conn.ehlo()

    msg = MIMEText(context, _charset="utf-8")
    msg['From'] = SMTP_EMAIL
    msg['To'] = to
    msg['Subject'] = title

    conn.login(SMTP_EMAIL, SMTP_PWD)
    conn.sendmail(SMTP_EMAIL, to, msg.as_string())
    conn.close()