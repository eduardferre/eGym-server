from pydantic import BaseModel

class UserTO(BaseModel):
    id: str
    username: str
    firstname: str
    lastname: str
    email: str
    password: str
    birthDate: str