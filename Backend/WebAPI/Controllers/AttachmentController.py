from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from Backend.WebAPI.Models.AttachmentModel import AttachmentModel
from Backend.WebAPI.Mappers.AttachmentMapper import AttachmentMapper
from Backend.Service.Services.Attachments.IAttachmentService import IAttachmentService
from Backend.Service.Services.Attachments.AttachmentDTO import AttachmentDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class AttachmentController(BaseController[AttachmentModel, AttachmentDTO]):
    def __init__(self, router: APIRouter, attachment_service: IAttachmentService):
        super().__init__(router, "attachments")
        self.attachment_service = attachment_service
        self._setup_upload_route()
    
    def _setup_upload_route(self):
        @self.router.post(f"/{self.prefix}/upload", response_model=AttachmentModel)
        async def upload_file(task_id: str, user_id: str, file: UploadFile = File(...)):
            return await self.upload_file(task_id, user_id, file)
    
    async def upload_file(self, task_id: str, user_id: str, file: UploadFile) -> AttachmentModel:
        attachment = await self.attachment_service.upload_attachment(
            task_id=task_id,
            user_id=user_id,
            file_name=file.filename,
            file_type=file.content_type,
            file_size=file.size,
            file_url=""  # This will be set by the service
        )
        return AttachmentMapper.to_model(attachment)
    
    async def get_all(self) -> List[AttachmentModel]:
        attachments = await self.attachment_service.get_all_attachments()
        return AttachmentMapper.to_model_list(attachments)
    
    async def get_by_id(self, id: str) -> AttachmentModel:
        attachment = await self.attachment_service.get_attachment_by_id(id)
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return AttachmentMapper.to_model(attachment)
    
    async def create(self, attachment: AttachmentDTO) -> AttachmentModel:
        created_attachment = await self.attachment_service.create_attachment(attachment)
        return AttachmentMapper.to_model(created_attachment)
    
    async def update(self, id: str, attachment: AttachmentDTO) -> AttachmentModel:
        updated_attachment = await self.attachment_service.update_attachment(id, attachment)
        if not updated_attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return AttachmentMapper.to_model(updated_attachment)
    
    async def delete(self, id: str):
        success = await self.attachment_service.delete_attachment(id)
        if not success:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return {"message": "Attachment deleted successfully"} 