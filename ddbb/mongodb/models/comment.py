from __future__ import annotations
from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    id: str
    creator: User
    content: str

from ddbb.mongodb.models.user import User
Comment.update_forward_refs()