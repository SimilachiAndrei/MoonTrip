from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Attachment:
    """Attachment entity representing a file attached to a task"""
    id: str
    task_id: str
    user_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime = field(default_factory=datetime.now)
