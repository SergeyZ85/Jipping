from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from src.database.engine import get_db
from src.schemas.finances import FinanceResponse, FinanceCreate, FinanceUpdate
from src.services.base_services import peoples_service, people_by_date_service, calculate_profit, FinanceService

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



@router.post("/", response_model=FinanceResponse, status_code=status.HTTP_201_CREATED)
def create_finance(
    finance: FinanceCreate,
    db: Session = Depends(get_db)
):
    service = FinanceService(db)
    return service.create_finance_record(finance)

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