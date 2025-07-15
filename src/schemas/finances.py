from pydantic import BaseModel
from datetime import date


class RegisterRequest(BaseModel):
    date_excursion: date
    count_peoples: int