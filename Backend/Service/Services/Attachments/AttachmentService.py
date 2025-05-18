from datetime import datetime
from typing import List, Optional
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Data.Entities.Attachment import Attachment
from Backend.Service.Services.Attachments.AttachmentDTO import AttachmentDTO
from Backend.Service.Mappers.AttachmentMapper import AttachmentMapper
from Backend.Service.Services.Attachments.IAttachmentService import IAttachmentService
from Backend.Service.Services.Activities.ActivityDTO import ActivityType

class AttachmentService(IAttachmentService):
    """Service for handling attachment operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def upload_attachment(self, task_id: str, user_id: str, file_name: str, file_type: str, file_size: int, file_url: str) -> AttachmentDTO:
        """Upload a new attachment"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Create attachment entity
            attachment = Attachment(
                id=None,  # Will be set by Firestore
                task_id=task_id,
                user_id=user_id,
                file_name=file_name,
                file_url=file_url,
                file_type=file_type,
                file_size=file_size,
                uploaded_at=datetime.utcnow(),
                metadata={}
            )
            
            # Add attachment
            self._uow.attachments.add(attachment)
            
            # Create activity
            activity_type = ActivityType.ATTACHMENT_ADDED
            metadata = {
                "attachment_id": attachment.id,
                "file_name": file_name,
                "file_type": file_type,
                "file_size": file_size
            }
            self._uow.activities.create_activity(task_id, user_id, activity_type, metadata)
            
            return AttachmentMapper.to_dto(attachment)
            
        except Exception as e:
            print(f"Error uploading attachment: {str(e)}")
            raise
    
    def get_attachment(self, attachment_id: str) -> Optional[AttachmentDTO]:
        """Get an attachment by ID"""
        try:
            attachment = self._uow.attachments.find_by_id(attachment_id)
            return AttachmentMapper.to_dto(attachment)
        except Exception as e:
            print(f"Error getting attachment: {str(e)}")
            return None
    
    def get_task_attachments(self, task_id: str, limit: Optional[int] = None) -> List[AttachmentDTO]:
        """Get all attachments for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get attachments
            attachments = self._uow.attachments.find_by_task(task_id)
            
            # Apply limit if specified
            if limit is not None:
                attachments = attachments[:limit]
            
            return AttachmentMapper.to_dto_list(attachments)
            
        except Exception as e:
            print(f"Error getting task attachments: {str(e)}")
            return []
    
    def get_user_attachments(self, user_id: str, limit: Optional[int] = None) -> List[AttachmentDTO]:
        """Get all attachments uploaded by a user"""
        try:
            # Validate user exists
            user = self._uow.users.find_by_id(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Get attachments
            attachments = self._uow.attachments.find_by_user(user_id)
            
            # Apply limit if specified
            if limit is not None:
                attachments = attachments[:limit]
            
            return AttachmentMapper.to_dto_list(attachments)
            
        except Exception as e:
            print(f"Error getting user attachments: {str(e)}")
            return []
    
    def delete_attachment(self, attachment_id: str) -> bool:
        """Delete an attachment"""
        try:
            attachment = self._uow.attachments.find_by_id(attachment_id)
            if not attachment:
                raise ValueError("Attachment not found")
            
            # Delete attachment
            self._uow.attachments.delete(attachment)
            
            # Create activity
            activity_type = ActivityType.ATTACHMENT_DELETED
            metadata = {
                "attachment_id": attachment.id,
                "file_name": attachment.file_name
            }
            self._uow.activities.create_activity(attachment.task_id, attachment.user_id, activity_type, metadata)
            
            return True
            
        except Exception as e:
            print(f"Error deleting attachment: {str(e)}")
            return False
    
    def get_attachments_by_type(self, task_id: str, file_type: str) -> List[AttachmentDTO]:
        """Get attachments of a specific type for a task"""
        try:
            # Validate task exists
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                raise ValueError("Task not found")
            
            # Get attachments
            attachments = self._uow.attachments.find_by_task(task_id)
            
            # Filter by type
            filtered_attachments = [
                attachment for attachment in attachments
                if attachment.file_type == file_type
            ]
            
            return AttachmentMapper.to_dto_list(filtered_attachments)
            
        except Exception as e:
            print(f"Error getting attachments by type: {str(e)}")
            return [] 