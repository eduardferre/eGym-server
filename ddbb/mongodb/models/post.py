from user import User
from comment import Comment

from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: str
    creator: User
    url: str
    caption: str
    likes: int
    comments: list(Comment)