from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.WebAPI.Models.CommentModel import CommentModel
from Backend.WebAPI.Mappers.CommentMapper import CommentMapper
from Backend.Service.Services.Comments.ICommentService import ICommentService
from Backend.Service.Services.Comments.CommentDTO import CommentDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class CommentController(BaseController[CommentModel, CommentDTO]):
    def __init__(self, router: APIRouter, comment_service: ICommentService):
        super().__init__(router, "comments")
        self.comment_service = comment_service
        self._setup_additional_routes()
    
    def _setup_additional_routes(self):
        @self.router.get(f"/{self.prefix}/task/{{task_id}}", response_model=List[CommentModel])
        async def get_by_task(task_id: str):
            return await self.get_by_task(task_id)
        
        @self.router.get(f"/{self.prefix}/user/{{user_id}}", response_model=List[CommentModel])
        async def get_by_user(user_id: str):
            return await self.get_by_user(user_id)
        
        @self.router.get(f"/{self.prefix}/{{id}}/replies", response_model=List[CommentModel])
        async def get_replies(id: str):
            return await self.get_replies(id)
    
    async def get_by_task(self, task_id: str) -> List[CommentModel]:
        comments = await self.comment_service.get_comments_by_task(task_id)
        return CommentMapper.to_model_list(comments)
    
    async def get_by_user(self, user_id: str) -> List[CommentModel]:
        comments = await self.comment_service.get_comments_by_user(user_id)
        return CommentMapper.to_model_list(comments)
    
    async def get_replies(self, id: str) -> List[CommentModel]:
        comment = await self.comment_service.get_comment_by_id(id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        replies = await self.comment_service.get_comment_replies(id)
        return CommentMapper.to_model_list(replies)
    
    async def get_all(self) -> List[CommentModel]:
        comments = await self.comment_service.get_all_comments()
        return CommentMapper.to_model_list(comments)
    
    async def get_by_id(self, id: str) -> CommentModel:
        comment = await self.comment_service.get_comment_by_id(id)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return CommentMapper.to_model(comment)
    
    async def create(self, comment: CommentDTO) -> CommentModel:
        created_comment = await self.comment_service.create_comment(comment)
        return CommentMapper.to_model(created_comment)
    
    async def update(self, id: str, comment: CommentDTO) -> CommentModel:
        updated_comment = await self.comment_service.update_comment(id, comment)
        if not updated_comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return CommentMapper.to_model(updated_comment)
    
    async def delete(self, id: str):
        success = await self.comment_service.delete_comment(id)
        if not success:
            raise HTTPException(status_code=404, detail="Comment not found")
        return {"message": "Comment deleted successfully"} 