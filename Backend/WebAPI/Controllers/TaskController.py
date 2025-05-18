from fastapi import APIRouter, Depends, HTTPException
from typing import List
from Backend.WebAPI.Models.TaskModel import TaskModel
from Backend.WebAPI.Mappers.TaskMapper import TaskMapper
from Backend.Service.Services.Tasks.ITaskService import ITaskService
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO
from Backend.WebAPI.Controllers.BaseController import BaseController

class TaskController(BaseController[TaskModel, TaskDTO]):
    def __init__(self, router: APIRouter, task_service: ITaskService):
        super().__init__(router, "tasks")
        self.task_service = task_service
        self._setup_additional_routes()
    
    def _setup_additional_routes(self):
        @self.router.get(f"/{self.prefix}/owner/{{owner_id}}", response_model=List[TaskModel])
        async def get_by_owner(owner_id: str):
            return await self.get_by_owner(owner_id)
        
        @self.router.get(f"/{self.prefix}/status/{{status}}", response_model=List[TaskModel])
        async def get_by_status(status: str):
            return await self.get_by_status(status)
        
        @self.router.get(f"/{self.prefix}/priority/{{priority}}", response_model=List[TaskModel])
        async def get_by_priority(priority: str):
            return await self.get_by_priority(priority)
        
        @self.router.get(f"/{self.prefix}/{{id}}/members", response_model=List[str])
        async def get_task_members(id: str):
            return await self.get_task_members(id)
    
    async def get_by_owner(self, owner_id: str) -> List[TaskModel]:
        tasks = await self.task_service.get_tasks_by_owner(owner_id)
        return TaskMapper.to_model_list(tasks)
    
    async def get_by_status(self, status: str) -> List[TaskModel]:
        tasks = await self.task_service.get_tasks_by_status(status)
        return TaskMapper.to_model_list(tasks)
    
    async def get_by_priority(self, priority: str) -> List[TaskModel]:
        tasks = await self.task_service.get_tasks_by_priority(priority)
        return TaskMapper.to_model_list(tasks)
    
    async def get_task_members(self, id: str) -> List[str]:
        task = await self.task_service.get_task_by_id(id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return [member.id for member in task.members]
    
    async def get_all(self) -> List[TaskModel]:
        tasks = await self.task_service.get_all_tasks()
        return TaskMapper.to_model_list(tasks)
    
    async def get_by_id(self, id: str) -> TaskModel:
        task = await self.task_service.get_task_by_id(id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskMapper.to_model(task)
    
    async def create(self, task: TaskDTO) -> TaskModel:
        created_task = await self.task_service.create_task(task)
        return TaskMapper.to_model(created_task)
    
    async def update(self, id: str, task: TaskDTO) -> TaskModel:
        updated_task = await self.task_service.update_task(id, task)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return TaskMapper.to_model(updated_task)
    
    async def delete(self, id: str):
        success = await self.task_service.delete_task(id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"} 