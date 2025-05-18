from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum
from Backend.Service.Services.Members.MemberDTO import MemberDTO
from Backend.Service.Services.Comments.CommentDTO import CommentDTO
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

class TaskPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class TaskDTO:
    """Data Transfer Object for Task entity"""
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
    
    # Related data
    members: List['MemberDTO'] = field(default_factory=list)
    comments: List['CommentDTO'] = field(default_factory=list)
    activities: List['ActivityDTO'] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)  # List of attachment URLs

@dataclass
class CreateTaskDTO:
    """Data Transfer Object for creating a new task"""
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    member_ids: List[str] = field(default_factory=list)  # List of user IDs to be added as members

@dataclass
class UpdateTaskDTO:
    """Data Transfer Object for updating an existing task"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    member_ids: Optional[List[str]] = None  # List of user IDs to be added as members

@dataclass
class TaskResponseDTO:
    """Data Transfer Object for task operation responses"""
    success: bool
    message: str
    task: Optional[TaskDTO] = None
    error_code: Optional[int] = None 