from typing import Optional
from .UserDTO import UserDTO
from .UserRequestDTO import RegisterUserDTO, UpdateUserDTO, UserResponseDTO

class IUserService:
    """Interface for user service operations"""
    
    def get_user_details(self, user_id: str) -> UserResponseDTO:
        """Get detailed user information"""
        ...
    
    def update_user_details(self, user_id: str, user_dto: UpdateUserDTO) -> UserResponseDTO:
        """Update user details"""
        ...
    
    def delete_user(self, user_id: str) -> UserResponseDTO:
        """Delete a user"""
        ...
    
    def register_user(self, user_dto: RegisterUserDTO, firebase_uid: str) -> UserResponseDTO:
        """Register a new user"""
        ...
    
    def get_user_by_email(self, email: str) -> Optional[UserDTO]:
        """Get user by email"""
        ...
    
    def get_user_by_username(self, username: str) -> Optional[UserDTO]:
        """Get user by username"""
        ... 