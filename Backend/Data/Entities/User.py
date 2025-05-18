from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """User entity representing a system user"""
    id: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    username: Optional[str] = None
    profile_picture: Optional[str] = None