from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class Task(BaseModel):
    id: str
    description: str
    status: TaskStatus = TaskStatus.PENDING
    priority: int = 1
    parent_task: Optional[str] = None
    subtasks: List[str] = []
    assigned_agent: Optional[str] = None
