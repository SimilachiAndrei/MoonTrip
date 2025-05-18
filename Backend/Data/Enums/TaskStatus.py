from enum import Enum

class TaskStatus(Enum):
    """Enum representing different task statuses"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"
    ACTIVE = "active"