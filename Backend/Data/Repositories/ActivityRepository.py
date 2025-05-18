from typing import List, Optional
from Backend.Data.Entities.Activity import Activity
from Backend.Data.Repositories.Repository.BaseRepository import BaseRepository

class ActivityRepository(BaseRepository[Activity]):
    """Repository for Activity entities"""
    
    def __init__(self):
        super().__init__('task_activities')
    
    def find_by_task(self, task_id: str) -> List[Activity]:
        """Find all activities for a specific task"""
        query = self.collection.where('task_id', '==', task_id)
        docs = query.stream()
        return [Activity(**doc.to_dict()) for doc in docs]
    
    def find_by_user(self, user_id: str) -> List[Activity]:
        """Find all activities performed by a specific user"""
        query = self.collection.where('user_id', '==', user_id)
        docs = query.stream()
        return [Activity(**doc.to_dict()) for doc in docs]
    
    def find_by_activity_type(self, activity_type: str) -> List[Activity]:
        """Find all activities of a specific type"""
        query = self.collection.where('activity_type', '==', activity_type)
        docs = query.stream()
        return [Activity(**doc.to_dict()) for doc in docs] 