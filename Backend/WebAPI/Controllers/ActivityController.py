from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.WebAPI.Models.ActivityModel import ActivityModel
from Backend.WebAPI.Mappers.ActivityMapper import ActivityMapper
from Backend.Service.Services.Activities.IActivityService import IActivityService
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class ActivityController(BaseController[ActivityModel, ActivityDTO]):
    def __init__(self, router: APIRouter, activity_service: IActivityService):
        super().__init__(router, "activities")
        self.activity_service = activity_service
        self._setup_additional_routes()
    
    def _setup_additional_routes(self):
        @self.router.get(f"/{self.prefix}/task/{{task_id}}", response_model=List[ActivityModel])
        async def get_by_task(task_id: str):
            return await self.get_by_task(task_id)
        
        @self.router.get(f"/{self.prefix}/user/{{user_id}}", response_model=List[ActivityModel])
        async def get_by_user(user_id: str):
            return await self.get_by_user(user_id)
        
        @self.router.get(f"/{self.prefix}/type/{{activity_type}}", response_model=List[ActivityModel])
        async def get_by_type(activity_type: str):
            return await self.get_by_type(activity_type)
    
    async def get_by_task(self, task_id: str) -> List[ActivityModel]:
        activities = await self.activity_service.get_activities_by_task(task_id)
        return ActivityMapper.to_model_list(activities)
    
    async def get_by_user(self, user_id: str) -> List[ActivityModel]:
        activities = await self.activity_service.get_activities_by_user(user_id)
        return ActivityMapper.to_model_list(activities)
    
    async def get_by_type(self, activity_type: str) -> List[ActivityModel]:
        activities = await self.activity_service.get_activities_by_type(activity_type)
        return ActivityMapper.to_model_list(activities)
    
    async def get_all(self) -> List[ActivityModel]:
        activities = await self.activity_service.get_all_activities()
        return ActivityMapper.to_model_list(activities)
    
    async def get_by_id(self, id: str) -> ActivityModel:
        activity = await self.activity_service.get_activity_by_id(id)
        if not activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return ActivityMapper.to_model(activity)
    
    async def create(self, activity: ActivityDTO) -> ActivityModel:
        created_activity = await self.activity_service.create_activity(activity)
        return ActivityMapper.to_model(created_activity)
    
    async def update(self, id: str, activity: ActivityDTO) -> ActivityModel:
        updated_activity = await self.activity_service.update_activity(id, activity)
        if not updated_activity:
            raise HTTPException(status_code=404, detail="Activity not found")
        return ActivityMapper.to_model(updated_activity)
    
    async def delete(self, id: str):
        success = await self.activity_service.delete_activity(id)
        if not success:
            raise HTTPException(status_code=404, detail="Activity not found")
        return {"message": "Activity deleted successfully"} 