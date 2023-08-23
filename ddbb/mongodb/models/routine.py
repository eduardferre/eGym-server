from user import User
from exercise import Exercise

import datetime

from pydantic import BaseModel
from typing import Optional

# User entity
class Routine(BaseModel):
    id: str
    creator: User
    name: str
    description: Optional (str)
    exercises: list(Exercise)
    liftedWeight: float
    date: datetime