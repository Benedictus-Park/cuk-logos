from config import DB_URL
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(DB_URL, pool_pre_ping=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.metadata = MetaData()
Base.query = db_session.query_property()

def init_database():
    from models import User, Member, DutyLog, Authcode, Duty
    
    Base.metadata.create_all(engine)