from db.sqlDB.models.exerciseTO import ExerciseTO

from pydantic import BaseModel
from typing import Optional


class RoutineTO(BaseModel):
    id: str
    creator: str
    name: str
    description: Optional[str]
    exercises: list[ExerciseTO]
