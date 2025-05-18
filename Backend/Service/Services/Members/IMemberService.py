from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from Backend.Service.Services.Members.MemberDTO import MemberDTO, MemberRole

class IMemberService(ABC):
    """Interface for Member service operations"""
    
    @abstractmethod
    def add_member(self, project_id: str, user_id: str, role: MemberRole, invited_by: Optional[str] = None) -> MemberDTO:
        """Add a new member to a project"""
        pass
    
    @abstractmethod
    def get_member(self, member_id: str) -> Optional[MemberDTO]:
        """Get a member by ID"""
        pass
    
    @abstractmethod
    def get_project_members(self, project_id: str, limit: Optional[int] = None) -> List[MemberDTO]:
        """Get all members of a project"""
        pass
    
    @abstractmethod
    def get_user_memberships(self, user_id: str, limit: Optional[int] = None) -> List[MemberDTO]:
        """Get all project memberships for a user"""
        pass
    
    @abstractmethod
    def update_member_role(self, member_id: str, new_role: MemberRole) -> Optional[MemberDTO]:
        """Update a member's role"""
        pass
    
    @abstractmethod
    def remove_member(self, member_id: str) -> bool:
        """Remove a member from a project"""
        pass
    
    @abstractmethod
    def deactivate_member(self, member_id: str) -> bool:
        """Deactivate a member's membership"""
        pass
    
    @abstractmethod
    def reactivate_member(self, member_id: str) -> bool:
        """Reactivate a member's membership"""
        pass
    
    @abstractmethod
    def update_last_active(self, member_id: str) -> bool:
        """Update member's last active timestamp"""
        pass 