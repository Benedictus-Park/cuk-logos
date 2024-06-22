from ..db import Base
from datetime import datetime
from sqlalchemy import Column, Integer, Date

class DutyLog:
    __tablename__ = "duty_log"
    id = Column(Integer, autoincrement=True, primary_key=True)
    uid = Column(Integer, nullable=False)
    duty_type = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    def __init__(self, uid:int, duty_type:int, date:str):
        self.uid = uid
        self.duty_type = duty_type
        self.date = datetime.strftime(date, "%Y%m%d") # Format must be YYYYMMDD