from typing import Optional
from ...Data.Entities.User import User
from ..Services.Users.UserDTO import UserDTO
from ..Services.Users.UserRequestDTO import RegisterUserDTO, UpdateUserDTO
from ..Services.Tasks.TaskDTO import TaskDTO
from ..Services.Activities.ActivityDTO import ActivityDTO
from ..Services.Comments.CommentDTO import CommentDTO
from ..Services.Members.MemberDTO import MemberDTO

class UserMapper:
    """Mapper for converting between User entity and DTOs"""
    
    @staticmethod
    def to_dto(entity: User, 
               owned_tasks: list[TaskDTO] = None,
               member_tasks: list[MemberDTO] = None,
               comments: list[CommentDTO] = None,
               activities: list[ActivityDTO] = None) -> UserDTO:
        """Convert User entity to UserDTO"""
        if entity is None:
            return None
            
        return UserDTO(
            id=entity.id,
            email=entity.email,
            created_at=entity.created_at,
            last_login=entity.last_login,
            username=entity.username,
            profile_picture=entity.profile_picture,
            owned_tasks=owned_tasks or [],
            member_tasks=member_tasks or [],
            comments=comments or [],
            activities=activities or []
        )
    
    @staticmethod
    def to_entity(dto: RegisterUserDTO, user_id: str) -> User:
        """Convert RegisterUserDTO to User entity"""
        if dto is None:
            return None
            
        return User(
            id=user_id,
            email=dto.email,
            username=dto.username,
            profile_picture=dto.profile_picture
        )
    
    @staticmethod
    def update_entity(entity: User, dto: UpdateUserDTO) -> User:
        """Update User entity with UpdateUserDTO values"""
        if entity is None or dto is None:
            return entity
            
        if dto.email is not None:
            entity.email = dto.email
        if dto.username is not None:
            entity.username = dto.username
        if dto.profile_picture is not None:
            entity.profile_picture = dto.profile_picture
            
        return entity 