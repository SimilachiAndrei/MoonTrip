from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T = TypeVar('T')

class IRepository(Generic[T], ABC):
    """Base repository interface defining common CRUD operations"""
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities of type T"""
        pass
    
    @abstractmethod
    def find_by_id(self, id: str) -> Optional[T]:
        """Find an entity by its ID"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> None:
        """Update an existing entity"""
        pass
    
    @abstractmethod
    def delete(self, entity: T) -> None:
        """Delete an entity"""
        pass
    
    @abstractmethod
    def add(self, entity: T) -> None:
        """Add a new entity"""
        pass 