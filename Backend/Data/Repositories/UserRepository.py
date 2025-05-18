from typing import Optional, List
from Backend.Data.Entities.User import User
from Backend.Data.Repositories.Repository.BaseRepository import BaseRepository

class UserRepository(BaseRepository[User]):
    """Repository for User entities"""
    
    def __init__(self):
        super().__init__('users')
    
    def find_by_email(self, email: str) -> Optional[User]:
        """Find a user by their email address"""
        query = self.collection.where('email', '==', email).limit(1)
        docs = query.stream()
        for doc in docs:
            return User(**doc.to_dict())
        return None
    
    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by their username"""
        query = self.collection.where('username', '==', username).limit(1)
        docs = query.stream()
        for doc in docs:
            return User(**doc.to_dict())
        return None 