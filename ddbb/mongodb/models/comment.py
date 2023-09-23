from __future__ import annotations
from pydantic import BaseModel
from typing import Optional


class Comment(BaseModel):
    id: str
    postId: str
    creator: str
    content: str
