from sqlalchemy import Column, Integer, Float, Date, String
from src.database.engine import Base

class Peoples(Base):
    __tablename__ = 'peoples'
    id = Column(Integer, primary_key=True)
    date=Column(Date)
    count_peoples = Column(Integer)


class Finances(Base):
    __tablename__ = "finances"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    people_count = Column(Integer)
    income = Column(Float)
    expenses = Column(Float, default=0)
    description = Column(String(500), default="")




