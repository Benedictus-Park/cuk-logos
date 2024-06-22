from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from .models import *
from config import DB_URL

engine = create_engine(DB_URL)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata = MetaData()
Base.query = db_session.query_property()

def init_database():
    from models import User, Member, DutyLog
    
    Base.metadata.create_all(engine)