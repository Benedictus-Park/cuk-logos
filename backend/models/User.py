from db import Base
from sqlalchemy import Column, Integer, VARCHAR

class User(Base):
    __tablename__ = "user"

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)
    email = Column(VARCHAR(320), nullable=False, unique=True)
    pwd = Column(VARCHAR(60), nullable=False)

    def __init__(self, name:str, email:str, pwd:str):
        self.name = name
        self.email = email
        self.pwd = pwd