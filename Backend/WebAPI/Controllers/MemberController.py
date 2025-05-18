from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.WebAPI.Models.MemberModel import MemberModel
from Backend.WebAPI.Mappers.MemberMapper import MemberMapper
from Backend.Service.Services.Members.IMemberService import IMemberService
from Backend.Service.Services.Members.MemberDTO import MemberDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class MemberController(BaseController[MemberModel, MemberDTO]):
    def __init__(self, router: APIRouter, member_service: IMemberService):
        super().__init__(router, "members")
        self.member_service = member_service
        self._setup_additional_routes()
    
    def _setup_additional_routes(self):
        @self.router.get(f"/{self.prefix}/project/{{project_id}}", response_model=List[MemberModel])
        async def get_by_project(project_id: str):
            return await self.get_by_project(project_id)
        
        @self.router.get(f"/{self.prefix}/user/{{user_id}}", response_model=List[MemberModel])
        async def get_by_user(user_id: str):
            return await self.get_by_user(user_id)
        
        @self.router.get(f"/{self.prefix}/role/{{role}}", response_model=List[MemberModel])
        async def get_by_role(role: str):
            return await self.get_by_role(role)
    
    async def get_by_project(self, project_id: str) -> List[MemberModel]:
        members = await self.member_service.get_members_by_project(project_id)
        return MemberMapper.to_model_list(members)
    
    async def get_by_user(self, user_id: str) -> List[MemberModel]:
        members = await self.member_service.get_members_by_user(user_id)
        return MemberMapper.to_model_list(members)
    
    async def get_by_role(self, role: str) -> List[MemberModel]:
        members = await self.member_service.get_members_by_role(role)
        return MemberMapper.to_model_list(members)
    
    async def get_all(self) -> List[MemberModel]:
        members = await self.member_service.get_all_members()
        return MemberMapper.to_model_list(members)
    
    async def get_by_id(self, id: str) -> MemberModel:
        member = await self.member_service.get_member_by_id(id)
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
        return MemberMapper.to_model(member)
    
    async def create(self, member: MemberDTO) -> MemberModel:
        created_member = await self.member_service.create_member(member)
        return MemberMapper.to_model(created_member)
    
    async def update(self, id: str, member: MemberDTO) -> MemberModel:
        updated_member = await self.member_service.update_member(id, member)
        if not updated_member:
            raise HTTPException(status_code=404, detail="Member not found")
        return MemberMapper.to_model(updated_member)
    
    async def delete(self, id: str):
        success = await self.member_service.delete_member(id)
        if not success:
            raise HTTPException(status_code=404, detail="Member not found")
        return {"message": "Member deleted successfully"} 