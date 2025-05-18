from datetime import datetime
from typing import List, Optional
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Data.Entities.Member import Member
from Backend.Service.Services.Members.MemberDTO import MemberDTO, MemberRole
from Backend.Service.Services.Members.IMemberService import IMemberService
from Backend.Service.Services.Activities.ActivityDTO import ActivityType

class MemberService(IMemberService):
    """Service for handling member operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def add_member(self, project_id: str, user_id: str, role: MemberRole, invited_by: Optional[str] = None) -> MemberDTO:
        """Add a new member to a project"""
        try:
            # Validate project exists
            project = self._uow.projects.find_by_id(project_id)
            if not project:
                raise ValueError("Project not found")
            
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Validate inviter if provided
            if invited_by:
                inviter = self._uow.users.find_by_id(invited_by)
                if not inviter:
                    raise ValueError("Inviter not found")
            
            # Check if user is already a member
            existing_member = self._uow.members.find_by_project_and_user(project_id, user_id)
            if existing_member:
                raise ValueError("User is already a member of this project")
            
            # Create member entity
            member = Member(
                id=None,  # Will be set by Firestore
                project_id=project_id,
                user_id=user_id,
                role=role,
                joined_at=datetime.utcnow(),
                invited_by=invited_by,
                is_active=True,
                last_active=datetime.utcnow(),
                metadata={}
            )
            
            # Add member
            self._uow.members.add(member)
            
            # Create activity
            activity_type = ActivityType.MEMBER_ADDED
            metadata = {
                "member_id": member.id,
                "role": role.value,
                "invited_by": invited_by
            }
            self._uow.activities.create_activity(project_id, user_id, activity_type, metadata)
            
            return self._to_dto(member)
            
        except Exception as e:
            print(f"Error adding member: {str(e)}")
            raise
    
    def get_member(self, member_id: str) -> Optional[MemberDTO]:
        """Get a member by ID"""
        try:
            member = self._uow.members.find_by_id(member_id)
            return self._to_dto(member) if member else None
        except Exception as e:
            print(f"Error getting member: {str(e)}")
            return None
    
    def get_project_members(self, project_id: str, limit: Optional[int] = None) -> List[MemberDTO]:
        """Get all members of a project"""
        try:
            # Validate project exists
            project = self._uow.projects.find_by_id(project_id)
            if not project:
                raise ValueError("Project not found")
            
            # Get members
            members = self._uow.members.find_by_project(project_id)
            
            # Apply limit if specified
            if limit is not None:
                members = members[:limit]
            
            return [self._to_dto(member) for member in members]
            
        except Exception as e:
            print(f"Error getting project members: {str(e)}")
            return []
    
    def get_user_memberships(self, user_id: str, limit: Optional[int] = None) -> List[MemberDTO]:
        """Get all project memberships for a user"""
        try:
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get memberships
            memberships = self._uow.members.find_by_user(user_id)
            
            # Apply limit if specified
            if limit is not None:
                memberships = memberships[:limit]
            
            return [self._to_dto(membership) for membership in memberships]
            
        except Exception as e:
            print(f"Error getting user memberships: {str(e)}")
            return []
    
    def update_member_role(self, member_id: str, new_role: MemberRole) -> Optional[MemberDTO]:
        """Update a member's role"""
        try:
            member = self._uow.members.find_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
            
            # Update role
            member.role = new_role
            self._uow.members.update(member)
            
            # Create activity
            activity_type = ActivityType.MEMBER_ROLE_UPDATED
            metadata = {
                "member_id": member.id,
                "new_role": new_role.value
            }
            self._uow.activities.create_activity(member.project_id, member.user_id, activity_type, metadata)
            
            return self._to_dto(member)
            
        except Exception as e:
            print(f"Error updating member role: {str(e)}")
            return None
    
    def remove_member(self, member_id: str) -> bool:
        """Remove a member from a project"""
        try:
            member = self._uow.members.find_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
            
            # Delete member
            self._uow.members.delete(member)
            
            # Create activity
            activity_type = ActivityType.MEMBER_REMOVED
            metadata = {"member_id": member.id}
            self._uow.activities.create_activity(member.project_id, member.user_id, activity_type, metadata)
            
            return True
            
        except Exception as e:
            print(f"Error removing member: {str(e)}")
            return False
    
    def deactivate_member(self, member_id: str) -> bool:
        """Deactivate a member's membership"""
        try:
            member = self._uow.members.find_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
            
            if not member.is_active:
                return True
            
            # Deactivate member
            member.is_active = False
            self._uow.members.update(member)
            
            # Create activity
            activity_type = ActivityType.MEMBER_DEACTIVATED
            metadata = {"member_id": member.id}
            self._uow.activities.create_activity(member.project_id, member.user_id, activity_type, metadata)
            
            return True
            
        except Exception as e:
            print(f"Error deactivating member: {str(e)}")
            return False
    
    def reactivate_member(self, member_id: str) -> bool:
        """Reactivate a member's membership"""
        try:
            member = self._uow.members.find_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
            
            if member.is_active:
                return True
            
            # Reactivate member
            member.is_active = True
            member.last_active = datetime.utcnow()
            self._uow.members.update(member)
            
            # Create activity
            activity_type = ActivityType.MEMBER_REACTIVATED
            metadata = {"member_id": member.id}
            self._uow.activities.create_activity(member.project_id, member.user_id, activity_type, metadata)
            
            return True
            
        except Exception as e:
            print(f"Error reactivating member: {str(e)}")
            return False
    
    def update_last_active(self, member_id: str) -> bool:
        """Update member's last active timestamp"""
        try:
            member = self._uow.members.find_by_id(member_id)
            if not member:
                raise ValueError("Member not found")
            
            member.last_active = datetime.utcnow()
            self._uow.members.update(member)
            return True
            
        except Exception as e:
            print(f"Error updating last active: {str(e)}")
            return False
    
    def _to_dto(self, member: Member) -> MemberDTO:
        """Convert Member entity to MemberDTO"""
        if member is None:
            return None
            
        return MemberDTO(
            id=member.id,
            user_id=member.user_id,
            project_id=member.project_id,
            role=member.role,
            joined_at=member.joined_at,
            invited_by=member.invited_by,
            is_active=member.is_active,
            last_active=member.last_active,
            metadata=member.metadata
        ) 