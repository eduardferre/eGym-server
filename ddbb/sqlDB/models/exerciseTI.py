from pydantic import BaseModel
from typing import Optional

# User entity
class ExerciseTI(BaseModel):
    id: str
    name: str
    description: Optional (str)