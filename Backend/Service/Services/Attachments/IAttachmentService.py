from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from .AttachmentDTO import AttachmentDTO

class IAttachmentService(ABC):
    """Interface for Attachment service operations"""
    
    @abstractmethod
    def upload_attachment(self, task_id: str, user_id: str, file_name: str, file_type: str, file_size: int, file_url: str) -> AttachmentDTO:
        """Upload a new attachment"""
        pass
    
    @abstractmethod
    def get_attachment(self, attachment_id: str) -> Optional[AttachmentDTO]:
        """Get an attachment by ID"""
        pass
    
    @abstractmethod
    def get_task_attachments(self, task_id: str, limit: Optional[int] = None) -> List[AttachmentDTO]:
        """Get all attachments for a task"""
        pass
    
    @abstractmethod
    def get_user_attachments(self, user_id: str, limit: Optional[int] = None) -> List[AttachmentDTO]:
        """Get all attachments uploaded by a user"""
        pass
    
    @abstractmethod
    def delete_attachment(self, attachment_id: str) -> bool:
        """Delete an attachment"""
        pass
    
    @abstractmethod
    def get_attachments_by_type(self, task_id: str, file_type: str) -> List[AttachmentDTO]:
        """Get attachments of a specific type for a task"""
        pass 