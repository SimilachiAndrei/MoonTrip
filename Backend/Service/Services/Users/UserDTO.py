from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO
from Backend.Service.Services.Members.MemberDTO import MemberDTO
from Backend.Service.Services.Comments.CommentDTO import CommentDTO
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO

@dataclass
class UserDTO:
    """Data Transfer Object for User entity"""
    id: str
    email: str
    created_at: datetime
    last_login: datetime = None
    username: str = None
    profile_picture: str = None
    
    # Related data
    owned_tasks: List[TaskDTO] = field(default_factory=list)
    member_tasks: List[MemberDTO] = field(default_factory=list)
    comments: List[CommentDTO] = field(default_factory=list)
    activities: List[ActivityDTO] = field(default_factory=list) 