from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TEXT, BIGINT

Base = declarative_base()

class Member(Base):
    __tablename__ = 'Member'
    id = Column(BIGINT, primary_key = True, nullable = False, autoincrement= False)
    name = Column(TEXT)
    avatar = Column(TEXT)
    member_type = Column(INTEGER, default = 0)

class Bag(Base):
    __tablename__ = 'Bag'
    id = Column(INTEGER, primary_key = True, nullable = False)
    server = Column(TEXT)


class BagItem(Base):
    __tablename__ = 'BagItem'
    id = Column(INTEGER, primary_key = True, nullable = False)
    bag_id = Column(INTEGER, ForeignKey('Bag.id'))
    item = Column(TEXT)