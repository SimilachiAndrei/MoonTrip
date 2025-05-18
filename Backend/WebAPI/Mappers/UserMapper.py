from typing import Optional, List
from Backend.WebAPI.Models.UserModel import UserModel
from Backend.Service.Services.Users.UserDTO import UserDTO

class UserMapper:
    @staticmethod
    def to_model(dto: UserDTO) -> Optional[UserModel]:
        if dto is None:
            return None
            
        return UserModel(
            id=dto.id,
            email=dto.email,
            username=dto.username,
            display_name=dto.display_name,
            profile_picture_url=dto.profile_picture_url,
            bio=dto.bio,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            last_login=dto.last_login,
            is_active=dto.is_active,
            firebase_uid=dto.firebase_uid,
            owned_tasks=[task.id for task in dto.owned_tasks] if dto.owned_tasks else [],
            member_tasks=[task.id for task in dto.member_tasks] if dto.member_tasks else [],
            comments=[comment.id for comment in dto.comments] if dto.comments else [],
            activities=[activity.id for activity in dto.activities] if dto.activities else []
        )
    
    @staticmethod
    def to_dto(model: UserModel) -> Optional[UserDTO]:
        if model is None:
            return None
            
        return UserDTO(
            id=model.id,
            email=model.email,
            username=model.username,
            display_name=model.display_name,
            profile_picture_url=model.profile_picture_url,
            bio=model.bio,
            created_at=model.created_at,
            updated_at=model.updated_at,
            last_login=model.last_login,
            is_active=model.is_active,
            firebase_uid=model.firebase_uid,
            owned_tasks=[],  # These will be populated by the service
            member_tasks=[],
            comments=[],
            activities=[]
        )
    
    @staticmethod
    def to_model_list(dtos: List[UserDTO]) -> List[UserModel]:
        return [UserMapper.to_model(dto) for dto in dtos if dto is not None]
    
    @staticmethod
    def to_dto_list(models: List[UserModel]) -> List[UserDTO]:
        return [UserMapper.to_dto(model) for model in models if model is not None] 