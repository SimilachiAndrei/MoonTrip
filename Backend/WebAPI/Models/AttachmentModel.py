from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel

class AttachmentModel(BaseModel):
    id: str
    task_id: str
    user_id: str
    file_name: str
    file_url: str
    file_type: str
    file_size: int
    uploaded_at: datetime
    metadata: Dict = {} 