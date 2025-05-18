from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from ..Enums.TaskStatus import TaskStatus

@dataclass
class Task:
    """Task entity representing a task in the system"""
    id: str
    title: str
    description: str
    owner_id: str
    status: TaskStatus = TaskStatus.ACTIVE
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    due_date: Optional[datetime] = None
    priority: Optional[int] = None
    tags: List[str] = field(default_factory=list) 