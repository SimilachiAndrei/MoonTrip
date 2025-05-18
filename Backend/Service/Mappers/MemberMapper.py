from typing import Optional, List
from ...Data.Entities.Member import Member
from ..Services.Members.MemberDTO import MemberDto, MemberRole

class MemberMapper:
    """Mapper for converting between Member entity and MemberDto"""
    
    @staticmethod
    def to_dto(member: Member) -> Optional[MemberDto]:
        """Convert Member entity to MemberDto"""
        if member is None:
            return None
            
        return MemberDto(
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
    
    @staticmethod
    def to_entity(dto: MemberDto) -> Member:
        """Convert MemberDto to Member entity"""
        if dto is None:
            return None
            
        return Member(
            id=dto.id,
            user_id=dto.user_id,
            project_id=dto.project_id,
            role=dto.role,
            joined_at=dto.joined_at,
            invited_by=dto.invited_by,
            is_active=dto.is_active,
            last_active=dto.last_active,
            metadata=dto.metadata
        )
    
    @staticmethod
    def to_dto_list(members: List[Member]) -> List[MemberDto]:
        """Convert a list of Member entities to MemberDto objects"""
        return [MemberMapper.to_dto(member) for member in members if member is not None] 