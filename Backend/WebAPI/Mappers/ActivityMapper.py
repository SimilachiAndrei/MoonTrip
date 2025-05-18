from typing import Optional, List
from Backend.WebAPI.Models.ActivityModel import ActivityModel
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO

class ActivityMapper:
    @staticmethod
    def to_model(dto: ActivityDTO) -> Optional[ActivityModel]:
        if dto is None:
            return None
            
        return ActivityModel(
            id=dto.id,
            task_id=dto.task_id,
            user_id=dto.user_id,
            activity_type=dto.activity_type,
            created_at=dto.created_at,
            metadata=dto.metadata
        )
    
    @staticmethod
    def to_dto(model: ActivityModel) -> Optional[ActivityDTO]:
        if model is None:
            return None
            
        return ActivityDTO(
            id=model.id,
            task_id=model.task_id,
            user_id=model.user_id,
            activity_type=model.activity_type,
            created_at=model.created_at,
            metadata=model.metadata
        )
    
    @staticmethod
    def to_model_list(dtos: List[ActivityDTO]) -> List[ActivityModel]:
        return [ActivityMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[ActivityModel]) -> List[ActivityDTO]:
        return [ActivityMapper.to_dto(model) for model in models if model is not None] 