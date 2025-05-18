from typing import List, Optional
from datetime import datetime

from Backend.Service.Services.Activities import ActivityDTO
from Backend.Data.Enums import ActivityType
class IActivityService:
    """Interface for activity service operations"""
    
    def create_activity(self, task_id: str, user_id: str, activity_type: ActivityType, metadata: dict) -> ActivityDTO:
        """Create a new activity"""
        ...
    
    def get_task_activities(self, task_id: str, limit: Optional[int] = None) -> List[ActivityDTO]:
        """Get all activities for a task"""
        ...
    
    def get_user_activities(self, user_id: str, limit: Optional[int] = None) -> List[ActivityDTO]:
        """Get all activities performed by a user"""
        ...
    
    def get_activities_by_type(self, task_id: str, activity_type: ActivityType) -> List[ActivityDTO]:
        """Get activities of a specific type for a task"""
        ...
    
    def get_activities_by_date_range(self, task_id: str, start_date: datetime, end_date: datetime) -> List[ActivityDTO]:
        """Get activities within a date range for a task"""
        ...
    
    def delete_activity(self, activity_id: str) -> bool:
        """Delete a specific activity"""
        ...
    
    def delete_task_activities(self, task_id: str) -> bool:
        """Delete all activities for a task"""
        ... 