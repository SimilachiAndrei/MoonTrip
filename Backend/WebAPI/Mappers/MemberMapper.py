from typing import Optional, List
from Backend.WebAPI.Models.MemberModel import MemberModel
from Backend.Service.Services.Members.MemberDTO import MemberDTO

class MemberMapper:
    @staticmethod
    def to_model(dto: MemberDTO) -> Optional[MemberModel]:
        if dto is None:
            return None
            
        return MemberModel(
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
    def to_dto(model: MemberModel) -> Optional[MemberDTO]:
        if model is None:
            return None
            
        return MemberDTO(
            id=model.id,
            user_id=model.user_id,
            project_id=model.project_id,
            role=model.role,
            joined_at=model.joined_at,
            invited_by=model.invited_by,
            is_active=model.is_active,
            last_active=model.last_active,
            metadata=model.metadata
        )
    
    @staticmethod
    def to_model_list(dtos: List[MemberDTO]) -> List[MemberModel]:
        return [MemberMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[MemberModel]) -> List[MemberDTO]:
        return [MemberMapper.to_dto(model) for model in models if model is not None] 