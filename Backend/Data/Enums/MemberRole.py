from enum import Enum

class MemberRole(Enum):
    """Enum representing different member roles"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer" 