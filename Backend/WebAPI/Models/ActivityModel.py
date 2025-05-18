from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel
from Backend.Data.Enums.ActivityType import ActivityType

class ActivityModel(BaseModel):
    id: str
    task_id: str
    user_id: str
    activity_type: ActivityType
    created_at: datetime
    metadata: Dict[str, Any] = {} 