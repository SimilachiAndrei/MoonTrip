from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .CommentDTO import CommentDTO

class ICommentService(ABC):
    """Interface for Comment service operations"""
    
    @abstractmethod
    def create_comment(self, task_id: str, user_id: str, content: str, parent_comment_id: Optional[str] = None) -> CommentDTO:
        """Create a new comment"""
        pass
    
    @abstractmethod
    def get_comment(self, comment_id: str) -> Optional[CommentDTO]:
        """Get a comment by ID"""
        pass
    
    @abstractmethod
    def get_task_comments(self, task_id: str, limit: Optional[int] = None) -> List[CommentDTO]:
        """Get all comments for a task"""
        pass
    
    @abstractmethod
    def get_user_comments(self, user_id: str, limit: Optional[int] = None) -> List[CommentDTO]:
        """Get all comments by a user"""
        pass
    
    @abstractmethod
    def update_comment(self, comment_id: str, content: str) -> Optional[CommentDTO]:
        """Update a comment's content"""
        pass
    
    @abstractmethod
    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment"""
        pass
    
    @abstractmethod
    def get_replies(self, comment_id: str) -> List[CommentDTO]:
        """Get all replies to a comment"""
        pass 