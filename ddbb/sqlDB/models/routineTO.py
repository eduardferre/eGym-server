from exerciseTO import ExerciseTO

from pydantic import BaseModel
from typing import Optional

# User entity
class RoutineTO(BaseModel):
    id: str
    creator: str
    name: str
    description: Optional (str)
    exercises: list(ExerciseTO)