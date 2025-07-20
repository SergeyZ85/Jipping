from datetime import date
from sqlalchemy import text

from fastapi import Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.database.db_queryes import get_total_people, get_people_by_date, get_income, get_expenses, FinanceQueries
from src.database.engine import get_db
from src.schemas.finances import FinanceUpdate, FinanceCreate


def peoples_service(result:dict=Depends(get_total_people)):
    return result

def people_by_date_service(target_date: date, count: int = Depends(get_people_by_date)):
    return {"date": target_date.isoformat(), "count": count}


def calculate_profit(
        start_date: date = None,
        end_date: date = None,
        db=Depends(get_db)
):
    income = get_income(db, start_date, end_date)
    expenses = get_expenses(db, start_date, end_date)

    return {
        "income": income,
        "expenses": expenses,
        "profit": income - expenses
    }

# Инициализируем Jinja2 шаблоны
templates = Jinja2Templates(directory="templates")

def html_service(request: Request, db=Depends(get_db)):
    # Получаем все записи о финансах
    trips = db.execute(text("SELECT * FROM finances ORDER BY date DESC")).fetchall()
    
    # Подсчитываем статистику
    total_people = sum(trip.people_count for trip in trips if trip.people_count)
    total_trips = len(trips)
    total_income = sum(trip.income for trip in trips if trip.income)
    total_expenses = sum(trip.expenses for trip in trips if trip.expenses)
    total_profit = total_income - total_expenses
    
    # Возвращаем HTML страницу
    return templates.TemplateResponse("index.html", {
        "request": request,
        "trips": trips,
        "total_people": total_people,
        "total_trips": total_trips,
        "total_income": total_income,
        "total_expenses": total_expenses,
        "total_profit": total_profit
    })

class FinanceService:
    def __init__(self, db):
        self.queries = FinanceQueries(db)

    def create_finance_record(self, finance: FinanceCreate):
        return self.queries.create_finance(finance.dict())

    def update_finance_record(self, finance_id: int, updates: FinanceUpdate):
        return self.queries.update_finance(finance_id, updates.dict(exclude_unset=True))

    def delete_finance_record(self, finance_id: int):
        return self.queries.delete_finance(finance_id)