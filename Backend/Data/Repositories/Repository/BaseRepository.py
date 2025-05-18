from typing import Generic, TypeVar, List, Optional
from ...Database.FirestoreClient import FirestoreClient
from .IRepository import IRepository

T = TypeVar('T')

class BaseRepository(IRepository[T], Generic[T]):
    """Base repository implementation using Firestore"""
    
    def __init__(self, collection_name: str):
        """Initialize repository with Firestore collection name"""
        self._client = FirestoreClient()
        self.collection = self._client.get_collection(collection_name)
    
    def get_all(self) -> List[T]:
        """Get all entities from the collection"""
        docs = self.collection.stream()
        return [doc.to_dict() for doc in docs]
    
    def find_by_id(self, id: str) -> Optional[T]:
        """Find an entity by its ID"""
        doc = self.collection.document(id).get()
        return doc.to_dict() if doc.exists else None
    
    def update(self, entity: T) -> None:
        """Update an existing entity"""
        if hasattr(entity, 'id'):
            self.collection.document(entity.id).set(entity.__dict__)
    
    def delete(self, entity: T) -> None:
        """Delete an entity"""
        if hasattr(entity, 'id'):
            self.collection.document(entity.id).delete()
    
    def add(self, entity: T) -> None:
        """Add a new entity"""
        if hasattr(entity, 'id'):
            self.collection.document(entity.id).set(entity.__dict__)
        else:
            self.collection.add(entity.__dict__) 