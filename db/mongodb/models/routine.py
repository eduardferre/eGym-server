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

    def __eq__(self, other):
        if isinstance(other, Routine):
            return (
                self.id == other.id and
                self.creator == other.creator and
                self.name == other.name and
                self.description == other.description and
                self.exercises == other.exercises and
                self.liftedWeight == other.liftedWeight
            )
        return False


from db.mongodb.models.exercise import Exercise

Routine.update_forward_refs()
