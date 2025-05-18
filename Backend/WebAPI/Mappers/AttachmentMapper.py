from typing import Optional, List
from Backend.WebAPI.Models.AttachmentModel import AttachmentModel
from Backend.Service.Services.Attachments.AttachmentDTO import AttachmentDTO

class AttachmentMapper:
    @staticmethod
    def to_model(dto: AttachmentDTO) -> Optional[AttachmentModel]:
        if dto is None:
            return None
            
        return AttachmentModel(
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
    def to_dto(model: AttachmentModel) -> Optional[AttachmentDTO]:
        if model is None:
            return None
            
        return AttachmentDTO(
            id=model.id,
            task_id=model.task_id,
            user_id=model.user_id,
            file_name=model.file_name,
            file_url=model.file_url,
            file_type=model.file_type,
            file_size=model.file_size,
            uploaded_at=model.uploaded_at,
            metadata=model.metadata
        )
    
    @staticmethod
    def to_model_list(dtos: List[AttachmentDTO]) -> List[AttachmentModel]:
        return [AttachmentMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[AttachmentModel]) -> List[AttachmentDTO]:
        return [AttachmentMapper.to_dto(model) for model in models if model is not None] 