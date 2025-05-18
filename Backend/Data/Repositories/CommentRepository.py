from typing import List, Optional
from ..Entities.Comment import Comment
from .Repository.BaseRepository import BaseRepository

class CommentRepository(BaseRepository[Comment]):
    """Repository for Comment entities"""
    
    def __init__(self):
        super().__init__('task_comments')
    
    def find_by_task(self, task_id: str) -> List[Comment]:
        """Find all comments for a specific task"""
        query = self.collection.where('task_id', '==', task_id)
        docs = query.stream()
        return [Comment(**doc.to_dict()) for doc in docs]
    
    def find_by_user(self, user_id: str) -> List[Comment]:
        """Find all comments made by a specific user"""
        query = self.collection.where('user_id', '==', user_id)
        docs = query.stream()
        return [Comment(**doc.to_dict()) for doc in docs]
    
    def find_replies(self, parent_comment_id: str) -> List[Comment]:
        """Find all replies to a specific comment"""
        query = self.collection.where('parent_comment_id', '==', parent_comment_id)
        docs = query.stream()
        return [Comment(**doc.to_dict()) for doc in docs] 