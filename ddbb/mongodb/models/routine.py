from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class Routine(BaseModel):
    id: str
    creator: User
    name: str
    description: Optional[str]
    exercises: list[Exercise]
    liftedWeight: float
    date: datetime

from ddbb.mongodb.models.user import User
from ddbb.mongodb.models.exercise import Exercise
Routine.update_forward_refs()