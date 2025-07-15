from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from src.database.engine import get_db
from src.database.models import Peoples
from src.database.models import Finances
from fastapi import Depends

def get_total_people(db=Depends(get_db)):
    total = db.query(func.sum(Peoples.count_peoples)).scalar()
    return {"total_people": total or 0}

def get_people_by_date(target_date: date, db= Depends(get_db)):
    return db.query(Peoples).filter(Peoples.date == target_date).count()

def request_in_db(db: Session):
    return result

def get_income(db= Depends(get_db),start_date: date = None, end_date: date = None,):
    query = db.query(func.sum(Finances.amount))
    if start_date:
        query = query.filter(Finances.date >= start_date)
    if end_date:
        query = query.filter(Finances.date <= end_date)
    return query.scalar() or 0

def get_expenses(db= Depends(get_db),start_date: date = None, end_date: date = None):
    query = db.query(
        func.sum(Finances.driver_salary +
               Finances.fuel +
               Finances.people_percent +
               Finances.entry_percent)
    )
    if start_date:
        query = query.filter(Finances.date >= start_date)
    if end_date:
        query = query.filter(Finances.date <= end_date)
    return query.scalar() or 0
