from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from enum import Enum
@dataclass
class Activity:
    """Activity entity representing an activity log for a task"""
    id: str
    task_id: str
    user_id: str
    activity_type: str  # e.g., "created", "updated", "commented", "joined"
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict = field(default_factory=dict)  # Additional activity data 

    
class ActivityType(Enum):
    """Enum representing different types of activities"""
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    COMMENT_ADDED = "comment_added"
    COMMENT_UPDATED = "comment_updated"
    COMMENT_DELETED = "comment_deleted"
    ATTACHMENT_ADDED = "attachment_added"
    ATTACHMENT_DELETED = "attachment_deleted"
    STATUS_CHANGED = "status_changed"
    ASSIGNEE_CHANGED = "assignee_changed"
