from datetime import datetime
from uuid import uuid4
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(Enum):
    TODO = 1
    IN_PROGRESS = 2
    DONE = 3


class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Task(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    owner_id: str
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
