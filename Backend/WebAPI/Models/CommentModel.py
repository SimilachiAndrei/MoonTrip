from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

class CommentModel(BaseModel):
    id: str
    task_id: str
    user_id: str
    content: str
    created_at: datetime
    updated_at: datetime
    parent_comment_id: Optional[str] = None
    replies: List[str] = []  # List of reply comment IDs
    is_edited: bool = False
    is_deleted: bool = False 