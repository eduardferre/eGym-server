from pydantic import BaseModel
from datetime import datetime


class UserTO(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    email: str
    password: str
    birthDate: str
