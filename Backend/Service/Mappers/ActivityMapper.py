from typing import Optional, List
from Backend.Data.Entities.Activity import Activity
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO, ActivityType

class ActivityMapper:
    """Mapper for converting between Activity entity and ActivityDTO"""
    
    @staticmethod
    def to_dto(activity: Activity) -> Optional[ActivityDTO]:
        """Convert Activity entity to ActivityDTO"""
        if activity is None:
            return None
            
        return ActivityDTO(
            id=activity.id,
            task_id=activity.task_id,
            user_id=activity.user_id,
            activity_type=activity.activity_type,
            created_at=activity.created_at,
            metadata=activity.metadata
        )
    
    @staticmethod
    def to_entity(dto: ActivityDTO) -> Activity:
        """Convert ActivityDTO to Activity entity"""
        if dto is None:
            return None
            
        return Activity(
            id=dto.id,
            task_id=dto.task_id,
            user_id=dto.user_id,
            activity_type=dto.activity_type,
            created_at=dto.created_at,
            metadata=dto.metadata
        )
    
    @staticmethod
    def to_dto_list(activities: List[Activity]) -> List[ActivityDTO]:
        """Convert a list of Activity entities to ActivityDTO objects"""
        return [ActivityMapper.to_dto(activity) for activity in activities if activity is not None] 