from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    id: str
    creator: str
    url: str
    caption: Optional[str]
    likes: int
    comments: list[Comment]
    creationDate: Optional[datetime]

    def __eq__(self, other):
        if isinstance(other, Post):
            return (
                self.id == other.id
                and self.creator == other.creator
                and self.url == other.url
                and self.caption == other.caption
                and self.likes == other.likes
                and self.comments == other.comments
                and self.creationDate == other.creationDate
            )
        return False


from db.mongodb.models.comment import Comment

Post.update_forward_refs()
