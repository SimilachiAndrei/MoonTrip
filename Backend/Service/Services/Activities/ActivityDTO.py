from dataclasses import dataclass, field
from datetime import datetime
from Backend.Data.Enums.ActivityType import ActivityType

@dataclass
class ActivityDTO:
    """Data Transfer Object for Activity"""
    id: str
    task_id: str
    user_id: str
    activity_type: ActivityType
    created_at: datetime
    metadata: dict = field(default_factory=dict) 