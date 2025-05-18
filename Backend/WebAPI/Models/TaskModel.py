from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from Backend.Data.Enums.TaskStatus import TaskStatus
from Backend.Data.Enums.TaskPriority import TaskPriority

class TaskModel(BaseModel):
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    owner_id: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    tags: List[str] = []
    attachments: List[str] = []  # List of attachment IDs
    comments: List[str] = []  # List of comment IDs
    activities: List[str] = []  # List of activity IDs
    members: List[str] = []  # List of member IDs 