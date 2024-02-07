from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: str
    username: str
    fullname: str
    email: str
    phone: str
    age: int
    height: float  # cm
    weight: float  # kg
    physicalActivity: float
    role: str
    followers: list[str]
    following: list[str]
    postsLog: list[Post]
    routinesLog: list[Routine]
    routines: list[RoutineTO]
    profilePicture: str
    backgroundPicture: str
    public: bool  # TODO: Publicity for User, ExerciseTO and RoutineTO should be implemented


from db.mongodb.models.post import Post
from db.mongodb.models.routine import Routine
from db.sqlDB.models.routineTO import RoutineTO

User.update_forward_refs()
