from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
from .TaskDTO import TaskDTO,TaskStatus, TaskPriority

@dataclass
class CreateTaskDTO:
    """DTO for creating a new task"""
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: List[str] = None
    member_ids: List[str] = None

@dataclass
class UpdateTaskDTO:
    """DTO for updating task details"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    member_ids: Optional[List[str]] = None

@dataclass
class TaskResponseDTO:
    """DTO for task response with status"""
    success: bool
    message: str
    task: Optional['TaskDTO'] = None
    error_code: Optional[int] = None 