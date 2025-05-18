from typing import Optional, List
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO
from Backend.Service.Services.Tasks.TaskRequestDTO import CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO

class ITaskService:
    """Interface for task service operations"""
    
    def create_task(self, task_dto: CreateTaskDTO, owner_id: str) -> TaskResponseDTO:
        """Create a new task"""
        ...
    
    def get_task(self, task_id: str) -> TaskResponseDTO:
        """Get task by ID"""
        ...
    
    def update_task(self, task_id: str, task_dto: UpdateTaskDTO) -> TaskResponseDTO:
        """Update task details"""
        ...
    
    def delete_task(self, task_id: str) -> TaskResponseDTO:
        """Delete a task"""
        ...
    
    def get_user_tasks(self, user_id: str, include_member_tasks: bool = True) -> List[TaskDTO]:
        """Get all tasks for a user (owned and/or member tasks)"""
        ...
    
    def get_tasks_by_status(self, status: str, user_id: str) -> List[TaskDTO]:
        """Get tasks by status for a specific user"""
        ...
    
    def get_tasks_by_priority(self, priority: str, user_id: str) -> List[TaskDTO]:
        """Get tasks by priority for a specific user"""
        ...
    
    def search_tasks(self, query: str, user_id: str) -> List[TaskDTO]:
        """Search tasks by title or description"""
        ... 