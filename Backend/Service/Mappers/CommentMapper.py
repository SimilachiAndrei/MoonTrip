from datetime import datetime
from typing import Optional, List
from Backend.Data.Entities.Comment import Comment
from Backend.Service.Services.Comments.CommentDTO import CommentDTO

class CommentMapper:
    """Mapper for converting between Comment entity and CommentDTO"""
    
    @staticmethod
    def to_dto(comment: Comment) -> Optional[CommentDTO]:
        """Convert Comment entity to CommentDTO"""
        if comment is None:
            return None
            
        return CommentDTO(
            id=comment.id,
            task_id=comment.task_id,
            user_id=comment.user_id,
            content=comment.content,
            created_at=comment.created_at,
            updated_at=comment.updated_at,
            parent_comment_id=comment.parent_comment_id,
            is_edited=comment.is_edited,
            metadata=comment.metadata
        )
    
    @staticmethod
    def to_entity(dto: CommentDTO) -> Comment:
        """Convert CommentDTO to Comment entity"""
        if dto is None:
            return None
            
        return Comment(
            id=dto.id,
            task_id=dto.task_id,
            user_id=dto.user_id,
            content=dto.content,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            parent_comment_id=dto.parent_comment_id,
            is_edited=dto.is_edited,
            metadata=dto.metadata
        )
    
    @staticmethod
    def to_dto_list(comments: List[Comment]) -> List[CommentDTO]:
        """Convert a list of Comment entities to CommentDTO objects"""
        return [CommentMapper.to_dto(comment) for comment in comments if comment is not None] 