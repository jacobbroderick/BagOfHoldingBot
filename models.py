from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TEXT, BIGINT

Base = declarative_base()

class Event(Base):
    __tablename__ = 'event'
    id = Column(BIGINT, primary_key = True, nullable = False)
    name = Column(TEXT)
    server = Column(TEXT)
    date = Column(DATETIME)

class Attendance(Base):
    __tablename__ = 'attendance'
    id = Column(BIGINT, primary_key = True, nullable = False)
    member_id = Column(BIGINT)
    event_id = Column(BIGINT)

class Member(Base):
    __tablename__ = 'Member'
    id = Column(BIGINT, primary_key = True, nullable = False, autoincrement= False)
    name = Column(TEXT)
    avatar = Column(TEXT)
