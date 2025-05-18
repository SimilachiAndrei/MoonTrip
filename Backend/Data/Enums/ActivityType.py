from enum import Enum

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