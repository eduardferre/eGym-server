from pydantic import BaseModel
import datetime

# User entity
class UserTO(BaseModel):
    id: str
    username: str
    firstname: str
    surname: str
    email: str
    password: str
    birthDate: datetime