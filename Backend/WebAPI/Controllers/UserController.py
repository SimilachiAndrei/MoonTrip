from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.WebAPI.Models.UserModel import UserModel
from Backend.WebAPI.Mappers.UserMapper import UserMapper
from Backend.Service.Services.Users.IUserService import IUserService
from Backend.Service.Services.Users.UserDTO import UserDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class UserController(BaseController[UserModel, UserDTO]):
    def __init__(self, router: APIRouter, user_service: IUserService):
        super().__init__(router, "users")
        self.user_service = user_service
        self._setup_additional_routes()
    
    def _setup_additional_routes(self):
        @self.router.get(f"/{self.prefix}/email/{{email}}", response_model=UserModel)
        async def get_by_email(email: str):
            return await self.get_by_email(email)
        
        @self.router.get(f"/{self.prefix}/username/{{username}}", response_model=UserModel)
        async def get_by_username(username: str):
            return await self.get_by_username(username)
        
        @self.router.get(f"/{self.prefix}/{{id}}/tasks", response_model=List[str])
        async def get_user_tasks(id: str):
            return await self.get_user_tasks(id)
    
    async def get_by_email(self, email: str) -> UserModel:
        user = await self.user_service.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserMapper.to_model(user)
    
    async def get_by_username(self, username: str) -> UserModel:
        user = await self.user_service.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserMapper.to_model(user)
    
    async def get_user_tasks(self, id: str) -> List[str]:
        user = await self.user_service.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return [task.id for task in user.owned_tasks] + [task.id for task in user.member_tasks]
    
    async def get_all(self) -> List[UserModel]:
        users = await self.user_service.get_all_users()
        return UserMapper.to_model_list(users)
    
    async def get_by_id(self, id: str) -> UserModel:
        user = await self.user_service.get_user_by_id(id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserMapper.to_model(user)
    
    async def create(self, user: UserDTO) -> UserModel:
        created_user = await self.user_service.create_user(user)
        return UserMapper.to_model(created_user)
    
    async def update(self, id: str, user: UserDTO) -> UserModel:
        updated_user = await self.user_service.update_user(id, user)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserMapper.to_model(updated_user)
    
    async def delete(self, id: str):
        success = await self.user_service.delete_user(id)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"} 