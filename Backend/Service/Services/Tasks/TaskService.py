from datetime import datetime
from typing import List, Optional
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Data.Entities.Task import Task
from Backend.Service.Services.Tasks.ITaskService import ITaskService
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO, CreateTaskDTO, UpdateTaskDTO, TaskResponseDTO
from Backend.Service.Services.Activities.ActivityDTO import ActivityType
from Backend.Service.Mappers.TaskMapper import TaskMapper

class TaskService(ITaskService):
    """Service for handling task operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def create_task(self, task_dto: CreateTaskDTO, owner_id: str) -> TaskResponseDTO:
        """Create a new task"""
        try:
            # Validate owner exists
            owner = self._uow.users.find_by_id(owner_id)
            if not owner:
                return TaskResponseDTO(
                    success=False,
                    message="Task owner not found",
                    error_code=404
                )
            
            # Create task entity
            task = Task(
                id=None,  # Will be set by Firestore
                title=task_dto.title,
                description=task_dto.description,
                status=task_dto.status,
                priority=task_dto.priority,
                owner_id=owner_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                due_date=task_dto.due_date,
                tags=task_dto.tags or [],
                attachments=[]
            )
            
            # Add task
            self._uow.tasks.add(task)
            
            # Add owner as task member if member_ids provided
            if task_dto.member_ids:
                # Add owner to member_ids if not already included
                if owner_id not in task_dto.member_ids:
                    task_dto.member_ids.append(owner_id)
                
                # Add all members
                for member_id in task_dto.member_ids:
                    member = self._uow.users.find_by_id(member_id)
                    if member:
                        self._uow.task_members.add_member(task.id, member_id, "member")
            
            # Create activity for task creation
            self._uow.activities.create_activity(
                task.id,
                owner_id,
                ActivityType.TASK_CREATED,
                {"task_title": task.title}
            )
            
            return TaskResponseDTO(
                success=True,
                message="Task created successfully",
                task=TaskMapper.to_dto(task)
            )
            
        except Exception as e:
            return TaskResponseDTO(
                success=False,
                message=f"Error creating task: {str(e)}",
                error_code=500
            )
    
    def get_task(self, task_id: str) -> TaskResponseDTO:
        """Get task by ID"""
        try:
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                return TaskResponseDTO(
                    success=False,
                    message="Task not found",
                    error_code=404
                )
            
            return TaskResponseDTO(
                success=True,
                message="Task retrieved successfully",
                task=TaskMapper.to_dto(task)
            )
            
        except Exception as e:
            return TaskResponseDTO(
                success=False,
                message=f"Error retrieving task: {str(e)}",
                error_code=500
            )
    
    def update_task(self, task_id: str, task_dto: UpdateTaskDTO) -> TaskResponseDTO:
        """Update task details"""
        try:
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                return TaskResponseDTO(
                    success=False,
                    message="Task not found",
                    error_code=404
                )
            
            # Track changes for activity logging
            changes = {}
            
            # Update task fields
            if task_dto.title is not None and task_dto.title != task.title:
                changes["title"] = {"old": task.title, "new": task_dto.title}
                task.title = task_dto.title
                
            if task_dto.description is not None and task_dto.description != task.description:
                changes["description"] = {"old": task.description, "new": task_dto.description}
                task.description = task_dto.description
                
            if task_dto.status is not None and task_dto.status != task.status:
                changes["status"] = {"old": task.status, "new": task_dto.status}
                task.status = task_dto.status
                
            if task_dto.priority is not None and task_dto.priority != task.priority:
                changes["priority"] = {"old": task.priority, "new": task_dto.priority}
                task.priority = task_dto.priority
                
            if task_dto.due_date is not None and task_dto.due_date != task.due_date:
                changes["due_date"] = {"old": task.due_date, "new": task_dto.due_date}
                task.due_date = task_dto.due_date
                
            if task_dto.tags is not None and task_dto.tags != task.tags:
                changes["tags"] = {"old": task.tags, "new": task_dto.tags}
                task.tags = task_dto.tags
            
            task.updated_at = datetime.utcnow()
            
            # Update task
            self._uow.tasks.update(task)
            
            # Update members if provided
            if task_dto.member_ids is not None:
                # Get current members
                current_members = self._uow.task_members.find_by_task(task_id)
                current_member_ids = {member.user_id for member in current_members}
                
                # Add new members
                for member_id in task_dto.member_ids:
                    if member_id not in current_member_ids:
                        member = self._uow.users.find_by_id(member_id)
                        if member:
                            self._uow.task_members.add_member(task.id, member_id, "member")
                            changes.setdefault("members", {}).setdefault("added", []).append(member_id)
                
                # Remove members not in the new list
                for member in current_members:
                    if member.user_id not in task_dto.member_ids and member.user_id != task.owner_id:
                        self._uow.task_members.remove_member(task.id, member.user_id)
                        changes.setdefault("members", {}).setdefault("removed", []).append(member.user_id)
            
            # Create activity for task update if there were changes
            if changes:
                self._uow.activities.create_activity(
                    task.id,
                    task.owner_id,
                    ActivityType.TASK_UPDATED,
                    {"changes": changes}
                )
            
            return TaskResponseDTO(
                success=True,
                message="Task updated successfully",
                task=TaskMapper.to_dto(task)
            )
            
        except Exception as e:
            return TaskResponseDTO(
                success=False,
                message=f"Error updating task: {str(e)}",
                error_code=500
            )
    
    def delete_task(self, task_id: str) -> TaskResponseDTO:
        """Delete a task"""
        try:
            task = self._uow.tasks.find_by_id(task_id)
            if not task:
                return TaskResponseDTO(
                    success=False,
                    message="Task not found",
                    error_code=404
                )
            
            # Delete task and all related data in a transaction
            with self._uow as uow:
                # Delete task members
                for member in uow.task_members.find_by_task(task_id):
                    uow.task_members.delete(member)
                
                # Delete task comments
                for comment in uow.task_comments.find_by_task(task_id):
                    uow.task_comments.delete(comment)
                
                # Delete task activities
                for activity in uow.task_activities.find_by_task(task_id):
                    uow.task_activities.delete(activity)
                
                # Delete task attachments
                for attachment in uow.attachments.find_by_task(task_id):
                    uow.attachments.delete(attachment)
                
                # Finally, delete the task
                uow.tasks.delete(task)
            
            return TaskResponseDTO(
                success=True,
                message="Task deleted successfully"
            )
            
        except Exception as e:
            return TaskResponseDTO(
                success=False,
                message=f"Error deleting task: {str(e)}",
                error_code=500
            )
    
    def get_user_tasks(self, user_id: str, include_member_tasks: bool = True) -> List[TaskDTO]:
        """Get all tasks for a user (owned and/or member tasks)"""
        try:
            tasks = []
            
            # Get owned tasks
            owned_tasks = self._uow.tasks.find_by_owner(user_id)
            tasks.extend([TaskMapper.to_dto(task) for task in owned_tasks])
            
            # Get member tasks if requested
            if include_member_tasks:
                member_tasks = self._uow.task_members.find_by_user(user_id)
                for member in member_tasks:
                    task = self._uow.tasks.find_by_id(member.task_id)
                    if task and task.owner_id != user_id:  # Don't duplicate owned tasks
                        tasks.append(TaskMapper.to_dto(task))
            
            return tasks
            
        except Exception as e:
            # Log error and return empty list
            print(f"Error getting user tasks: {str(e)}")
            return []
    
    def get_tasks_by_status(self, status: str, user_id: str) -> List[TaskDTO]:
        """Get tasks by status for a specific user"""
        try:
            tasks = self.get_user_tasks(user_id)
            return [task for task in tasks if task.status.value == status]
        except Exception as e:
            print(f"Error getting tasks by status: {str(e)}")
            return []
    
    def get_tasks_by_priority(self, priority: str, user_id: str) -> List[TaskDTO]:
        """Get tasks by priority for a specific user"""
        try:
            tasks = self.get_user_tasks(user_id)
            return [task for task in tasks if task.priority.value == priority]
        except Exception as e:
            print(f"Error getting tasks by priority: {str(e)}")
            return []
    
    def search_tasks(self, query: str, user_id: str) -> List[TaskDTO]:
        """Search tasks by title or description"""
        try:
            tasks = self.get_user_tasks(user_id)
            query = query.lower()
            return [
                task for task in tasks
                if query in task.title.lower() or query in task.description.lower()
            ]
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")
            return []
    
    def get_tasks_by_due_date(self, start_date: datetime, end_date: datetime, user_id: str) -> List[TaskDTO]:
        """Get tasks due between start_date and end_date"""
        try:
            tasks = self.get_user_tasks(user_id)
            return [
                task for task in tasks
                if task.due_date and start_date <= task.due_date <= end_date
            ]
        except Exception as e:
            print(f"Error getting tasks by due date: {str(e)}")
            return []
    
    def get_tasks_by_tag(self, tag: str, user_id: str) -> List[TaskDTO]:
        """Get tasks with a specific tag"""
        try:
            tasks = self.get_user_tasks(user_id)
            return [task for task in tasks if tag in task.tags]
        except Exception as e:
            print(f"Error getting tasks by tag: {str(e)}")
            return []
    
    def get_overdue_tasks(self, user_id: str) -> List[TaskDTO]:
        """Get all overdue tasks for a user"""
        try:
            tasks = self.get_user_tasks(user_id)
            now = datetime.utcnow()
            return [
                task for task in tasks
                if task.due_date and task.due_date < now and task.status.value != "completed"
            ]
        except Exception as e:
            print(f"Error getting overdue tasks: {str(e)}")
            return [] 