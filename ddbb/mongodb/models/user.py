from post import Post
from routine import Routine

from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    fullname: str
    email: str
    age: int
    height: float #cm
    weight: float #kg
    physicalActiviy: float
    role: str
    followers: int
    postsLog: list(Post)
    routinesLog: list(Routine)
    profilePicture: str
    backgroundPicture: str