from pydantic import BaseModel
from typing import Optional

class Set(BaseModel):
    id: str
    exerciseName: str
    weight: int
    reps: int
    rpe: float
    rir: int
    restTime: float