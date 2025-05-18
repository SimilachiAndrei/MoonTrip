from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class CommentDTO:
    """Data Transfer Object for Comment"""
    id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    parent_comment_id: Optional[str] = None
    is_edited: bool = False
    metadata: dict = field(default_factory=dict) 