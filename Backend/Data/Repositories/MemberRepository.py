from typing import List, Optional
from ..Entities.Member import Member
from .Repository.BaseRepository import BaseRepository

class MemberRepository(BaseRepository[Member]):
    """Repository for Member entities"""
    
    def __init__(self):
        super().__init__('task_members')
    
    def find_by_task(self, task_id: str) -> List[Member]:
        """Find all members of a specific task"""
        query = self.collection.where('task_id', '==', task_id)
        docs = query.stream()
        return [Member(**doc.to_dict()) for doc in docs]
    
    def find_by_user(self, user_id: str) -> List[Member]:
        """Find all tasks a user is a member of"""
        query = self.collection.where('user_id', '==', user_id)
        docs = query.stream()
        return [Member(**doc.to_dict()) for doc in docs]

    
    def find_by_task_and_user(self, task_id: str, user_id: str) -> Optional[Member]:
        """Find a specific task member by task and user IDs"""
        query = self.collection.where('task_id', '==', task_id).where('user_id', '==', user_id).limit(1)
        docs = query.stream()
        for doc in docs:
            return Member(**doc.to_dict())
        return None 