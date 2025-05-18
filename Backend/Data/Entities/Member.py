from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Member:
    """Member entity representing a user's membership in a task"""
    id: str
    user_id: str
    task_id: str
    joined_at: datetime = field(default_factory=datetime.now)
    role: Optional[str] = None  # e.g., "admin", "member", "viewer" 