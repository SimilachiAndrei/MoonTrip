from typing import Optional
import re
from datetime import datetime
from Backend.Data.UnitOfWork.IUnitOfWork import IUnitOfWork
from Backend.Service.Services.Users.UserDTO import UserDTO
from Backend.Service.Services.Users.UserRequestDTO import RegisterUserDTO, UpdateUserDTO, UserResponseDTO
from Backend.Service.Services.Tasks.TaskDTO import TaskDTO
from Backend.Service.Services.Members.MemberDTO import MemberDTO
from Backend.Service.Services.Comments.CommentDTO import CommentDTO
from Backend.Service.Services.Activities.ActivityDTO import ActivityDTO
from Backend.Service.Mappers.UserMapper import UserMapper
from Backend.Service.Services.Users.IUserService import IUserService

class UserService(IUserService):
    """Service for handling user operations"""
    
    def __init__(self, unit_of_work: IUnitOfWork):
        self._uow = unit_of_work
    
    def get_user_details(self, user_id: str) -> UserResponseDTO:
        """Get detailed user information"""
        try:
            # Get user
            user = self._uow.users.find_by_id(user_id)
            if not user:
                return UserResponseDTO(
                    success=False,
                    message="User not found",
                    error_code=404
                )
            
            # Get related data
            owned_tasks = [TaskDTO(**task.__dict__) for task in self._uow.tasks.find_by_owner(user_id)]
            member_tasks = [MemberDTO(**member.__dict__) for member in self._uow.task_members.find_by_user(user_id)]
            comments = [CommentDTO(**comment.__dict__) for comment in self._uow.task_comments.find_by_user(user_id)]
            activities = [ActivityDTO(**activity.__dict__) for activity in self._uow.task_activities.find_by_user(user_id)]
            
            # Map to DTO
            user_dto = UserMapper.to_dto(
                user,
                owned_tasks=owned_tasks,
                member_tasks=member_tasks,
                comments=comments,
                activities=activities
            )
            
            return UserResponseDTO(
                success=True,
                message="User details retrieved successfully",
                user=user_dto
            )
            
        except Exception as e:
            return UserResponseDTO(
                success=False,
                message=f"Error retrieving user details: {str(e)}",
                error_code=500
            )
    
    def update_user_details(self, user_id: str, user_dto: UpdateUserDTO) -> UserResponseDTO:
        """Update user details"""
        try:
            # Validate email if provided
            if user_dto.email and not self._is_valid_email(user_dto.email):
                return UserResponseDTO(
                    success=False,
                    message="Invalid email format",
                    error_code=400
                )
            
            # Check if email is already taken
            if user_dto.email:
                existing_user = self._uow.users.find_by_email(user_dto.email)
                if existing_user and existing_user.id != user_id:
                    return UserResponseDTO(
                        success=False,
                        message="Email already in use",
                        error_code=409
                    )
            
            # Check if username is already taken
            if user_dto.username:
                existing_user = self._uow.users.find_by_username(user_dto.username)
                if existing_user and existing_user.id != user_id:
                    return UserResponseDTO(
                        success=False,
                        message="Username already in use",
                        error_code=409
                    )
            
            # Get and update user
            user = self._uow.users.find_by_id(user_id)
            if not user:
                return UserResponseDTO(
                    success=False,
                    message="User not found",
                    error_code=404
                )
            
            updated_user = UserMapper.update_entity(user, user_dto)
            self._uow.users.update(updated_user)
            
            return UserResponseDTO(
                success=True,
                message="User details updated successfully",
                user=UserMapper.to_dto(updated_user)
            )
            
        except Exception as e:
            return UserResponseDTO(
                success=False,
                message=f"Error updating user details: {str(e)}",
                error_code=500
            )
    
    def delete_user(self, user_id: str) -> UserResponseDTO:
        """Delete a user"""
        try:
            user = self._uow.users.find_by_id(user_id)
            if not user:
                return UserResponseDTO(
                    success=False,
                    message="User not found",
                    error_code=404
                )
            
            # Delete user's tasks, comments, etc.
            with self._uow as uow:
                # Delete user's tasks
                for task in uow.tasks.find_by_owner(user_id):
                    uow.tasks.delete(task)
                
                # Delete user's task memberships
                for member in uow.task_members.find_by_user(user_id):
                    uow.task_members.delete(member)
                
                # Delete user's comments
                for comment in uow.task_comments.find_by_user(user_id):
                    uow.task_comments.delete(comment)
                
                # Delete user's activities
                for activity in uow.task_activities.find_by_user(user_id):
                    uow.task_activities.delete(activity)
                
                # Finally, delete the user
                uow.users.delete(user)
            
            return UserResponseDTO(
                success=True,
                message="User deleted successfully"
            )
            
        except Exception as e:
            return UserResponseDTO(
                success=False,
                message=f"Error deleting user: {str(e)}",
                error_code=500
            )
    
    def register_user(self, user_dto: RegisterUserDTO, firebase_uid: str) -> UserResponseDTO:
        """Register a new user"""
        try:
            # Validate email
            if not self._is_valid_email(user_dto.email):
                return UserResponseDTO(
                    success=False,
                    message="Invalid email format",
                    error_code=400
                )
            
            # Check if email is already taken
            if self._uow.users.find_by_email(user_dto.email):
                return UserResponseDTO(
                    success=False,
                    message="Email already in use",
                    error_code=409
                )
            
            # Check if username is already taken
            if user_dto.username and self._uow.users.find_by_username(user_dto.username):
                return UserResponseDTO(
                    success=False,
                    message="Username already in use",
                    error_code=409
                )
            
            # Create user
            user = UserMapper.to_entity(user_dto, firebase_uid)
            self._uow.users.add(user)
            
            return UserResponseDTO(
                success=True,
                message="User registered successfully",
                user=UserMapper.to_dto(user)
            )
            
        except Exception as e:
            return UserResponseDTO(
                success=False,
                message=f"Error registering user: {str(e)}",
                error_code=500
            )
    
    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        """Get user by email"""
        user = self._uow.users.find_by_email(email)
        return UserMapper.to_dto(user) if user else None
    
    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        """Get user by username"""
        user = self._uow.users.find_by_username(username)
        return UserMapper.to_dto(user) if user else None
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) 