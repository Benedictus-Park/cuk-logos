from ..db import Base
from sqlalchemy import Column, Integer, VARCHAR

class Authcode(Base):
    __tablename__ = "authcode"

    authcode = Column(Integer, nullable=False, primary_key=True)
    name = Column(VARCHAR(15), nullable=False)

    def __init__(self, name:str, authcode:int):
        self.name = name
        self.authcode = authcode