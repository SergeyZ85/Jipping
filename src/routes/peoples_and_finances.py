from datetime import date

from fastapi import APIRouter, Depends

from src.services.base_services import peoples_service, people_by_date_service, calculate_profit

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
