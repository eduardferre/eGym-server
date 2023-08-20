from pydantic import BaseModel
from typing import Optional
import datetime

# User entity
class UserTI(BaseModel):
    id: str
    username: str
    firstname: str
    surname: str
    email: str
    password: str
    birthDate: datetime