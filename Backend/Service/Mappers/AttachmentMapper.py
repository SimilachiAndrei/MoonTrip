from typing import Optional, List
from ...Data.Entities.Attachment import Attachment
from ..Services.Attachments.AttachmentDTO import AttachmentDTO

class AttachmentMapper:
    """Mapper for converting between Attachment entity and AttachmentDTO"""
    
    @staticmethod
    def to_dto(attachment: Attachment) -> Optional[AttachmentDTO]:
        """Convert Attachment entity to AttachmentDTO"""
        if attachment is None:
            return None
            
        return AttachmentDTO(
            id=attachment.id,
            task_id=attachment.task_id,
            user_id=attachment.user_id,
            file_name=attachment.file_name,
            file_url=attachment.file_url,
            file_type=attachment.file_type,
            file_size=attachment.file_size,
            uploaded_at=attachment.uploaded_at,
            metadata=attachment.metadata
        )
    
    @staticmethod
    def to_entity(dto: AttachmentDTO) -> Attachment:
        """Convert AttachmentDTO to Attachment entity"""
        if dto is None:
            return None
            
        return Attachment(
            id=dto.id,
            task_id=dto.task_id,
            user_id=dto.user_id,
            file_name=dto.file_name,
            file_url=dto.file_url,
            file_type=dto.file_type,
            file_size=dto.file_size,
            uploaded_at=dto.uploaded_at,
            metadata=dto.metadata
        )
    
    @staticmethod
    def to_dto_list(attachments: List[Attachment]) -> List[AttachmentDTO]:
        """Convert a list of Attachment entities to AttachmentDTO objects"""
        return [AttachmentMapper.to_dto(attachment) for attachment in attachments if attachment is not None] 