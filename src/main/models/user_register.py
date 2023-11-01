from pydantic import BaseModel
from typing import Optional


class UserRegister(BaseModel):
    username: str
    password: str
    firstname: str
    lastname: str
    fullname: str
    email: str
    phone: str
    birthDate: str
    age: int
    height: float
    weight: float
    physicalActivity: float
    role: str
    followers: list[None]
    following: list[None]
    postsLog: list[None]
    routinesLog: list[None]
    routines: list[None]
    profilePicture: str
    backgroundPicture: str
    public: bool
