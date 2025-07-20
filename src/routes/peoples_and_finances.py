from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from starlette import status
from fastapi.responses import HTMLResponse, RedirectResponse

from src.database.engine import get_db
from src.schemas.finances import FinanceResponse, FinanceCreate, FinanceUpdate
from src.services.base_services import peoples_service, people_by_date_service, calculate_profit, FinanceService, html_service, templates

router = APIRouter()

@router.get("/total-people")
def get_total_people_count(result=Depends(peoples_service)):
    return result



@router.get("/people-by-date")
def get_people_count(
    target_date: date,
    result: dict = Depends(people_by_date_service)
):
    return result

@router.get("/profit")
def get_profit(
    start_date: date = None,
    end_date: date = None,
    profit_data: dict = Depends(calculate_profit)
):
    return profit_data

@router.get("/", response_class=HTMLResponse)
def get_finances(result = Depends(html_service)):
    return result

@router.post("/", response_class=HTMLResponse)
def create_finance_from_form(
    date: str = Form(...),
    people_count: int = Form(...),
    income: float = Form(...),
    expenses: float = Form(default=0),
    description: str = Form(default=""),
    db: Session = Depends(get_db)
):
    # Конвертируем строку даты в объект date
    from datetime import datetime
    trip_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Создаем объект FinanceCreate
    finance_data = FinanceCreate(
        date=trip_date,
        people_count=people_count,
        income=income,
        expenses=expenses,
        description=description
    )
    
    # Сохраняем в базу данных
    service = FinanceService(db)
    service.create_finance_record(finance_data)
    
    # Перенаправляем обратно на главную страницу
    return RedirectResponse(url="/", status_code=303)

@router.patch("/{finance_id}", response_model=FinanceResponse)
def update_finance(
    finance_id: int,
    updates: FinanceUpdate,
    db: Session = Depends(get_db)
):
    service = FinanceService(db)
    updated_finance = service.update_finance_record(finance_id, updates)
    if not updated_finance:
        raise HTTPException(status_code=404, detail="Finance record not found")
    return updated_finance

@router.delete("/{finance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finance(
    finance_id: int,
    db: Session = Depends(get_db)
):
    service = FinanceService(db)
    if not service.delete_finance_record(finance_id):
        raise HTTPException(status_code=404, detail="Finance record not found")