from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class Exercise(BaseModel):
    id: str
    name: str
    description: Optional[str]
    sets: list[Set]
    liftedWeight: float
    highestWeight: float

    

from db.mongodb.models.set import Set

Exercise.update_forward_refs()
