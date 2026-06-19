from datetime import datetime
from uuid import uuid4

from pydantic import EmailStr, BaseModel, Field


class User(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    username: str = Field(min_length=6)
    email: EmailStr
    created_at: datetime = Field(default_factory=datetime.now)
