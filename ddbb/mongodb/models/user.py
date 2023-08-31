from __future__ import annotations
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
    physicalActivity: float
    role: str
    followers: int
    postsLog: list[Post]
    routinesLog: list[Routine]
    profilePicture: str
    backgroundPicture: str


from ddbb.mongodb.models.post import Post
from ddbb.mongodb.models.routine import Routine
User.update_forward_refs()