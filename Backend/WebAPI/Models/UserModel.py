from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr
class UserModel(BaseModel):
    id: str
    email: EmailStr
    username: str
    display_name: str
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    firebase_uid: str
    owned_tasks: List[str] = []  # List of task IDs
    member_tasks: List[str] = []  # List of task IDs
    comments: List[str] = []  # List of comment IDs
    activities: List[str] = []  # List of activity IDs
