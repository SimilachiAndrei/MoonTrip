from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class AttachmentDTO:
    """Data Transfer Object for Attachment"""
    id: str
    task_id: str
    user_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    metadata: dict = field(default_factory=dict) 