from datetime import datetime
from typing import List, Optional
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Data.Entities.Comment import Comment
from Backend.Service.Services.Comments.CommentDTO import CommentDTO
from Backend.Service.Mappers.CommentMapper import CommentMapper
from Backend.Service.Services.Comments.ICommentService import ICommentService
from Backend.Service.Services.Activities.ActivityDTO import ActivityType

class CommentService(ICommentService):
    """Service for handling comment operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def create_comment(self, task_id: str, user_id: str, content: str, parent_comment_id: Optional[str] = None) -> CommentDTO:
        """Create a new comment"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Validate parent comment if provided
            if parent_comment_id:
                parent_comment = self._uow.comments.find_by_id(parent_comment_id)
                if not parent_comment:
                    raise ValueError("Parent comment not found")
            
            # Create comment entity
            comment = Comment(
                id=None,  # Will be set by Firestore
                task_id=task_id,
                user_id=user_id,
                content=content,
                created_at=datetime.utcnow(),
                updated_at=None,
                parent_comment_id=parent_comment_id,
                is_edited=False,
                metadata={}
            )
            
            # Add comment
            self._uow.comments.add(comment)
            
            # Create activity
            activity_type = ActivityType.COMMENT_ADDED
            metadata = {
                "comment_id": comment.id,
                "parent_comment_id": parent_comment_id
            }
            self._uow.activities.create_activity(task_id, user_id, activity_type, metadata)
            
            return CommentMapper.to_dto(comment)
            
        except Exception as e:
            print(f"Error creating comment: {str(e)}")
            raise
    
    def get_comment(self, comment_id: str) -> Optional[CommentDTO]:
        """Get a comment by ID"""
        try:
            comment = self._uow.comments.find_by_id(comment_id)
            return CommentMapper.to_dto(comment)
        except Exception as e:
            print(f"Error getting comment: {str(e)}")
            return None
    
    def get_task_comments(self, task_id: str, limit: Optional[int] = None) -> List[CommentDTO]:
        """Get all comments for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get comments
            comments = self._uow.comments.find_by_task(task_id)
            
            # Apply limit if specified
            if limit is not None:
                comments = comments[:limit]
            
            return CommentMapper.to_dto_list(comments)
            
        except Exception as e:
            print(f"Error getting task comments: {str(e)}")
            return []
    
    def get_user_comments(self, user_id: str, limit: Optional[int] = None) -> List[CommentDTO]:
        """Get all comments by a user"""
        try:
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get comments
            comments = self._uow.comments.find_by_user(user_id)
            
            # Apply limit if specified
            if limit is not None:
                comments = comments[:limit]
            
            return CommentMapper.to_dto_list(comments)
            
        except Exception as e:
            print(f"Error getting user comments: {str(e)}")
            return []
    
    def update_comment(self, comment_id: str, content: str) -> Optional[CommentDTO]:
        """Update a comment's content"""
        try:
            comment = self._uow.comments.find_by_id(comment_id)
            if not comment:
                raise ValueError("Comment not found")
            
            # Update comment
            comment.content = content
            comment.updated_at = datetime.utcnow()
            comment.is_edited = True
            
            self._uow.comments.update(comment)
            
            # Create activity
            activity_type = ActivityType.COMMENT_UPDATED
            metadata = {"comment_id": comment.id}
            self._uow.activities.create_activity(comment.task_id, comment.user_id, activity_type, metadata)
            
            return CommentMapper.to_dto(comment)
            
        except Exception as e:
            print(f"Error updating comment: {str(e)}")
            return None
    
    def delete_comment(self, comment_id: str) -> bool:
        """Delete a comment"""
        try:
            comment = self._uow.comments.find_by_id(comment_id)
            if not comment:
                raise ValueError("Comment not found")
            
            # Delete comment
            self._uow.comments.delete(comment)
            
            # Create activity
            activity_type = ActivityType.COMMENT_DELETED
            metadata = {"comment_id": comment.id}
            self._uow.activities.create_activity(comment.task_id, comment.user_id, activity_type, metadata)
            
            return True
            
        except Exception as e:
            print(f"Error deleting comment: {str(e)}")
            return False
    
    def get_replies(self, comment_id: str) -> List[CommentDTO]:
        """Get all replies to a comment"""
        try:
            comment = self._uow.comments.find_by_id(comment_id)
            if not comment:
                raise ValueError("Comment not found")
            
            replies = self._uow.comments.find_replies(comment_id)
            return CommentMapper.to_dto_list(replies)
            
        except Exception as e:
            print(f"Error getting replies: {str(e)}")
            return [] 