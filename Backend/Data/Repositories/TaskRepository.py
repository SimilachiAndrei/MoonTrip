from typing import List, Optional
from ..Entities.Task import Task
from ..Enums.TaskStatus import TaskStatus
from .Repository.BaseRepository import BaseRepository

class TaskRepository(BaseRepository[Task]):
    """Repository for Task entities"""
    
    def __init__(self):
        super().__init__('tasks')
    
    def find_by_owner(self, owner_id: str) -> List[Task]:
        """Find all tasks owned by a specific user"""
        query = self.collection.where('owner_id', '==', owner_id)
        docs = query.stream()
        return [Task(**doc.to_dict()) for doc in docs]
    
    def find_by_status(self, status: TaskStatus) -> List[Task]:
        """Find all tasks with a specific status"""
        query = self.collection.where('status', '==', status.value)
        docs = query.stream()
        return [Task(**doc.to_dict()) for doc in docs]
    
    def find_by_tag(self, tag: str) -> List[Task]:
        """Find all tasks with a specific tag"""
        query = self.collection.where('tags', 'array_contains', tag)
        docs = query.stream()
        return [Task(**doc.to_dict()) for doc in docs]
    
    def find_by_priority(self, priority: int) -> List[Task]:
        """Find all tasks with a specific priority"""
        query = self.collection.where('priority', '==', priority)
        docs = query.stream()
        return [Task(**doc.to_dict()) for doc in docs] 