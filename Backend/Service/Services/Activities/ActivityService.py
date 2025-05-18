from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Data.Entities.Activity import Activity
from Backend.Service.Mappers.ActivityMapper import ActivityMapper
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO, ActivityType
from Backend.Service.Services.Activities.IActivityService import IActivityService


class ActivityService(IActivityService):
    """Service for handling activity operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def create_activity(self, task_id: str, user_id: str, activity_type: ActivityType, metadata: dict) -> ActivityDTO:
        """Create a new activity"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Create activity entity
            activity = Activity(
                id=None,  # Will be set by Firestore
                task_id=task_id,
                user_id=user_id,
                activity_type=activity_type,
                created_at=datetime.utcnow(),
                metadata=metadata
            )
            
            # Add activity
            self._uow.activities.add(activity)
            
            return ActivityMapper.to_dto(activity)
            
        except Exception as e:
            print(f"Error creating activity: {str(e)}")
            raise
    
    def get_task_activities(self, task_id: str, limit: Optional[int] = None) -> List[ActivityDTO]:
        """Get all activities for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get activities
            activities = self._uow.activities.find_by_task(task_id)
            
            # Apply limit if specified
            if limit is not None:
                activities = activities[:limit]
            
            return ActivityMapper.to_dto_list(activities)
            
        except Exception as e:
            print(f"Error getting task activities: {str(e)}")
            return []
    
    def get_user_activities(self, user_id: str, limit: Optional[int] = None) -> List[ActivityDTO]:
        """Get all activities performed by a user"""
        try:
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get activities
            activities = self._uow.activities.find_by_user(user_id)
            
            # Apply limit if specified
            if limit is not None:
                activities = activities[:limit]
            
            return ActivityMapper.to_dto_list(activities)
            
        except Exception as e:
            print(f"Error getting user activities: {str(e)}")
            return []
    
    def get_activities_by_type(self, task_id: str, activity_type: ActivityType) -> List[ActivityDTO]:
        """Get activities of a specific type for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get activities
            activities = self._uow.activities.find_by_task(task_id)
            
            # Filter by type
            filtered_activities = [
                activity for activity in activities
                if activity.activity_type == activity_type
            ]
            
            return ActivityMapper.to_dto_list(filtered_activities)
            
        except Exception as e:
            print(f"Error getting activities by type: {str(e)}")
            return []
    
    def get_activities_by_date_range(self, task_id: str, start_date: datetime, end_date: datetime) -> List[ActivityDTO]:
        """Get activities within a date range for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Validate date range
            if start_date > end_date:
                raise ValueError("Start date must be before end date")
            
            # Get activities
            activities = self._uow.activities.find_by_task(task_id)
            
            # Filter by date range
            filtered_activities = [
                activity for activity in activities
                if start_date <= activity.created_at <= end_date
            ]
            
            return ActivityMapper.to_dto_list(filtered_activities)
            
        except Exception as e:
            print(f"Error getting activities by date range: {str(e)}")
            return []
    
    def delete_activity(self, activity_id: str) -> bool:
        """Delete a specific activity"""
        try:
            activity = self._uow.activities.find_by_id(activity_id)
            if not activity:
                raise ValueError("Activity not found")
            
            self._uow.activities.delete(activity)
            return True
            
        except Exception as e:
            print(f"Error deleting activity: {str(e)}")
            return False
    
    def delete_task_activities(self, task_id: str) -> bool:
        """Delete all activities for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get all activities for the task
            activities = self._uow.activities.find_by_task(task_id)
            
            # Delete all activities
            for activity in activities:
                self._uow.activities.delete(activity)
            
            return True
            
        except Exception as e:
            print(f"Error deleting task activities: {str(e)}")
            return False 