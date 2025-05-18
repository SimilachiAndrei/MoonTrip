from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel
from Backend.Data.Enums.MemberRole import MemberRole

class MemberModel(BaseModel):
    id: str
    user_id: str
    project_id: str
    role: MemberRole
    joined_at: datetime
    invited_by: Optional[str] = None
    is_active: bool = True
    last_active: Optional[datetime] = None
    metadata: Dict = {} 