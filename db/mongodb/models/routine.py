from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Routine(BaseModel):
    id: str
    creator: str
    name: str
    description: Optional[str]
    exercises: list[Exercise]
    liftedWeight: float
    date: datetime


from db.mongodb.models.exercise import Exercise

Routine.update_forward_refs()
