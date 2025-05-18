from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from ..Users.UserDTO import UserDTO
@dataclass
class RegisterUserDTO:
    """DTO for user registration"""
    email: str
    username: Optional[str] = None
    profile_picture: Optional[str] = None

@dataclass
class UpdateUserDTO:
    """DTO for updating user details"""
    email: Optional[str] = None
    username: Optional[str] = None
    profile_picture: Optional[str] = None

@dataclass
class UserResponseDTO:
    """DTO for user response with status"""
    success: bool
    message: str
    user: Optional['UserDTO'] = None
    error_code: Optional[int] = None 