from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    id: str
    creator: User
    url: str
    caption: str
    likes: int
    comments: list[Comment]

from ddbb.mongodb.models.user import User
from ddbb.mongodb.models.comment import Comment
Post.update_forward_refs()