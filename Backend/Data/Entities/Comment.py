from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class Comment:
    """Comment entity representing a comment on a task"""
    id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    parent_comment_id: Optional[str] = None  # For nested comments 