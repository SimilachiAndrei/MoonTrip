from typing import Protocol
from Backend.Data.Repositories.UserRepository import UserRepository
from Backend.Data.Repositories.TaskRepository import TaskRepository
from Backend.Data.Repositories.MemberRepository import MemberRepository
from Backend.Data.Repositories.CommentRepository import CommentRepository
from Backend.Data.Repositories.AttachmentRepository import AttachmentRepository
from Backend.Data.Repositories.ActivityRepository import ActivityRepository

class IUnitOfWork(Protocol):
    """Interface defining the contract for Unit of Work pattern"""
    
    # Repository properties
    @property
    def users(self) -> UserRepository:
        """Get the user repository"""
        ...
    
    @property
    def tasks(self) -> TaskRepository:
        """Get the task repository"""
        ...
    
    @property
    def members(self) -> MemberRepository:
        """Get the task member repository"""
        ...
    
    @property
    def comments(self) -> CommentRepository:
        """Get the task comment repository"""
        ...
    
    @property
    def attachments(self) -> AttachmentRepository:
        """Get the task attachment repository"""
        ...
    
    @property
    def activities(self) -> ActivityRepository:
        """Get the task activity repository"""
        ...
    
    def commit(self) -> None:
        """Commit all changes to the database"""
        ...
    
    def rollback(self) -> None:
        """Rollback all changes"""
        ...
    
    def begin_transaction(self) -> None:
        """Begin a new transaction"""
        ...
    
    def end_transaction(self) -> None:
        """End the current transaction"""
        ... 