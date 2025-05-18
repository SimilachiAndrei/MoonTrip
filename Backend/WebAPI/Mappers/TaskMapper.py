from typing import Optional, List
from Backend.WebAPI.Models.TaskModel import TaskModel
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO

class TaskMapper:
    @staticmethod
    def to_model(dto: TaskDTO) -> Optional[TaskModel]:
        if dto is None:
            return None
            
        return TaskModel(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            status=dto.status,
            priority=dto.priority,
            owner_id=dto.owner_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            due_date=dto.due_date,
            completed_at=dto.completed_at,
            tags=dto.tags,
            attachments=[attachment.id for attachment in dto.attachments] if dto.attachments else [],
            comments=[comment.id for comment in dto.comments] if dto.comments else [],
            activities=[activity.id for activity in dto.activities] if dto.activities else [],
            members=[member.id for member in dto.members] if dto.members else []
        )
    
    @staticmethod
    def to_dto(model: TaskModel) -> Optional[TaskDTO]:
        if model is None:
            return None
            
        return TaskDTO(
            id=model.id,
            title=model.title,
            description=model.description,
            status=model.status,
            priority=model.priority,
            owner_id=model.owner_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
            due_date=model.due_date,
            completed_at=model.completed_at,
            tags=model.tags,
            attachments=[],  # These will be populated by the service
            comments=[],
            activities=[],
            members=[]
        )
    
    @staticmethod
    def to_model_list(dtos: List[TaskDTO]) -> List[TaskModel]:
        return [TaskMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[TaskModel]) -> List[TaskDTO]:
        return [TaskMapper.to_dto(model) for model in models if model is not None] 