from pydantic import BaseModel
from datetime import date


class RegisterRequest(BaseModel):
    date_excursion: date
    count_peoples: int

from typing import Optional

class FinanceCreate(BaseModel):
    date: date
    amount: float
    driver_salary: float
    fuel: float
    people_percent: float
    entry_percent: float

class FinanceUpdate(BaseModel):
    date: Optional[date] = None
    amount: Optional[float] = None
    driver_salary: Optional[float] = None
    fuel: Optional[float] = None
    people_percent: Optional[float] = None
    entry_percent: Optional[float] = None

class FinanceResponse(BaseModel):
    id: int
    date: date
    amount: float
    driver_salary: float
    fuel: float
    people_percent: float
    entry_percent: float