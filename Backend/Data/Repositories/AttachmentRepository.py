from typing import List, Optional
from ..Entities.Attachment import Attachment
from .Repository.BaseRepository import BaseRepository
class AttachmentRepository(BaseRepository[Attachment]):
    """Repository for Attachment entities"""
    
    def __init__(self):
        super().__init__('task_attachments')
    
    def find_by_task(self, task_id: str) -> List[Attachment]:
        """Find all attachments for a specific task"""
        query = self.collection.where('task_id', '==', task_id)
        docs = query.stream()
        return [Attachment(**doc.to_dict()) for doc in docs]
    
    def find_by_user(self, user_id: str) -> List[Attachment]:
        """Find all attachments uploaded by a specific user"""
        query = self.collection.where('user_id', '==', user_id)
        docs = query.stream()
        return [Attachment(**doc.to_dict()) for doc in docs]
    
    def find_by_file_type(self, file_type: str) -> List[Attachment]:
        """Find all attachments of a specific file type"""
        query = self.collection.where('file_type', '==', file_type)
        docs = query.stream()
        return [Attachment(**doc.to_dict()) for doc in docs] 