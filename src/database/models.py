from sqlalchemy import Column, Integer, Float, Date
from src.database.engine import Base

class Peoples(Base):
    __tablename__ = 'Peoples'
    id = Column(Integer, primary_key=True)
    date=Column(Date)
    count_peoples = Column(Integer)


class Finances(Base):
    __tablename__ = "Finances"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    amount = Column(Float)
    driver_salary = Column(Float)
    fuel = Column(Float)
    people_percent = Column(Float)
    entry_percent = Column(Float)




