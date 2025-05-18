from typing import Optional, List
from ...Data.Entities.Task import Task
from ..Services.Tasks.TaskDTO import TaskDTO

class TaskMapper:
    """Mapper for converting between Task entity and TaskDTO"""
    
    @staticmethod
    def to_dto(task: Task) -> Optional[TaskDTO]:
        """Convert Task entity to TaskDTO"""
        if task is None:
            return None
            
        return TaskDTO(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            priority=task.priority,
            owner_id=task.owner_id,
            created_at=task.created_at,
            updated_at=task.updated_at,
            due_date=task.due_date,
            completed_at=task.completed_at,
            tags=task.tags,
            attachments=task.attachments
        )
    
    @staticmethod
    def to_entity(dto: TaskDTO) -> Task:
        """Convert TaskDTO to Task entity"""
        if dto is None:
            return None
            
        return Task(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            status=dto.status,
            priority=dto.priority,
            owner_id=dto.owner_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            due_date=dto.due_date,
            completed_at=dto.completed_at,
            tags=dto.tags,
            attachments=dto.attachments
        )
    
    @staticmethod
    def to_dto_list(tasks: List[Task]) -> List[TaskDTO]:
        """Convert a list of Task entities to TaskDTO objects"""
        return [TaskMapper.to_dto(task) for task in tasks if task is not None] 