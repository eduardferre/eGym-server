from user import User

from pydantic import BaseModel
from typing import Optional

class Comment(BaseModel):
    id: str
    creator: User
    content: str