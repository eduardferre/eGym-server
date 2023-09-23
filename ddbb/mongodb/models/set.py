from pydantic import BaseModel
from typing import Optional


class Set(BaseModel):
    id: str
    weight: int
    reps: int
    rpe: Optional[float]
    rir: Optional[int]
    restTime: Optional[float]