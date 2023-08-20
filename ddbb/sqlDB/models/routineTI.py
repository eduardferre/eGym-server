from pydantic import BaseModel
from typing import Optional
from exerciseTI import ExerciseTI

# User entity
class RoutineTI(BaseModel):
    id: str
    name: str
    description: Optional (str)
    exercises: list(ExerciseTI)