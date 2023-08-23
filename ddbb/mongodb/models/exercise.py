from set import Set

from pydantic import BaseModel
from typing import Optional

class Exercise(BaseModel):
    id: str
    name: str
    description: Optional (str)
    sets: list(Set)
    liftedWeight: float
    highestWeight: float