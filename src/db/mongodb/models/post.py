from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    id: str
    creator: str
    url: str
    caption: str
    likes: int
    comments: list[Comment]


from src.db.mongodb.models.comment import Comment

Post.update_forward_refs()
