from user import User
from exercise import Exercise

from datetime import datetime

from pydantic import BaseModel
from typing import Optional

class Routine(BaseModel):
    id: str
    creator: User
    name: str
    description: Optional (str)
    exercises: list(Exercise)
    liftedWeight: float
    date: datetime