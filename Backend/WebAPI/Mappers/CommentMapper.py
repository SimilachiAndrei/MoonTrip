from typing import Optional, List
from ..Models.CommentModel import CommentModel
from Backend.Service.Services.Comments.CommentDTO import CommentDTO

class CommentMapper:
    @staticmethod
    def to_model(dto: CommentDTO) -> Optional[CommentModel]:
        if dto is None:
            return None
            
        return CommentModel(
            id=dto.id,
            task_id=dto.task_id,
            user_id=dto.user_id,
            content=dto.content,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            parent_comment_id=dto.parent_comment_id,
            replies=[reply.id for reply in dto.replies] if dto.replies else [],
            is_edited=dto.is_edited,
            is_deleted=dto.is_deleted
        )
    
    @staticmethod
    def to_dto(model: CommentModel) -> Optional[CommentDTO]:
        if model is None:
            return None
            
        return CommentDTO(
            id=model.id,
            task_id=model.task_id,
            user_id=model.user_id,
            content=model.content,
            created_at=model.created_at,
            updated_at=model.updated_at,
            parent_comment_id=model.parent_comment_id,
            replies=[],  # These will be populated by the service
            is_edited=model.is_edited,
            is_deleted=model.is_deleted
        )
    
    @staticmethod
    def to_model_list(dtos: List[CommentDTO]) -> List[CommentModel]:
        return [CommentMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[CommentModel]) -> List[CommentDTO]:
        return [CommentMapper.to_dto(model) for model in models if model is not None] 