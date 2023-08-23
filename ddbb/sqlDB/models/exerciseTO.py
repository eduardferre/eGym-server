from pydantic import BaseModel
from typing import Optional

# User entity
class ExerciseTO(BaseModel):
    id: str
    name: str
    description: Optional (str)