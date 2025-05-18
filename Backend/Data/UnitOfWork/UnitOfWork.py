from typing import Optional
from google.cloud import firestore
from ..Database.FirestoreClient import FirestoreClient
from ..Repositories.UserRepository import UserRepository
from ..Repositories.TaskRepository import TaskRepository
from ..Repositories.MemberRepository import MemberRepository
from ..Repositories.CommentRepository import CommentRepository
from ..Repositories.AttachmentRepository import AttachmentRepository
from ..Repositories.ActivityRepository import ActivityRepository
from .IUnitOfWork import IUnitOfWork

class UnitOfWork(IUnitOfWork):
    """Implementation of Unit of Work pattern for Firestore"""
    
    def __init__(self):
        self._client = FirestoreClient()
        self._transaction: Optional[firestore.Transaction] = None
        
        # Initialize repositories
        self._user_repository = UserRepository()
        self._task_repository = TaskRepository()
        self._member_repository = MemberRepository()
        self._comment_repository = CommentRepository()
        self._attachment_repository = AttachmentRepository()
        self._activity_repository = ActivityRepository()
    
    @property
    def users(self) -> UserRepository:
        return self._user_repository
    
    @property
    def tasks(self) -> TaskRepository:
        return self._task_repository
    
    @property
    def members(self) -> MemberRepository:
        return self._member_repository
    
    @property
    def comments(self) -> CommentRepository:
        return self._comment_repository
    
    @property
    def attachments(self) -> AttachmentRepository:
        return self._attachment_repository
    
    @property
    def activities(self) -> ActivityRepository:
        return self._activity_repository
    
    def begin_transaction(self) -> None:
        """Begin a new Firestore transaction"""
        if self._transaction is not None:
            raise RuntimeError("Transaction already in progress")
        self._transaction = self._client.db.transaction()
    
    def commit(self) -> None:
        """Commit the current transaction"""
        if self._transaction is None:
            raise RuntimeError("No transaction in progress")
        try:
            self._transaction.commit()
        finally:
            self._transaction = None
    
    def rollback(self) -> None:
        """Rollback the current transaction"""
        if self._transaction is None:
            raise RuntimeError("No transaction in progress")
        self._transaction = None
    
    def end_transaction(self) -> None:
        """End the current transaction (commit or rollback)"""
        if self._transaction is not None:
            self.rollback()
    
    def __enter__(self):
        """Context manager entry"""
        self.begin_transaction()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is None:
            self.commit()
        else:
            self.rollback() 