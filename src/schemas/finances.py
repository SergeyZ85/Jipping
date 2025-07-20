from pydantic import BaseModel
from datetime import date


class RegisterRequest(BaseModel):
    date_excursion: date
    count_peoples: int

from typing import Optional

class FinanceCreate(BaseModel):
    date: date
    people_count: int
    income: float
    expenses: float = 0
    description: str = ""

class FinanceUpdate(BaseModel):
    date: Optional[date] = None
    people_count: Optional[int] = None
    income: Optional[float] = None
    expenses: Optional[float] = None
    description: Optional[str] = None

class FinanceResponse(BaseModel):
    id: int
    date: date
    people_count: int
    income: float
    expenses: float
    description: str