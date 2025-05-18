from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from Backend.Data.Enums.MemberRole import MemberRole

@dataclass
class MemberDTO:
    """Data Transfer Object for Member"""
    id: str
    user_id: str
    project_id: str
    role: MemberRole
    joined_at: datetime
    invited_by: Optional[str] = None
    is_active: bool = True
    last_active: Optional[datetime] = None
    metadata: dict = field(default_factory=dict) 