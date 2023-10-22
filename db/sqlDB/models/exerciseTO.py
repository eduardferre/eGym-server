from pydantic import BaseModel
from typing import Optional


class ExerciseTO(BaseModel):
    id: str
    creator: str
    name: str
    description: Optional[str]
