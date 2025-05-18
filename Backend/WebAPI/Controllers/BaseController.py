from typing import Generic, TypeVar, List, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)
U = TypeVar('U', bound=BaseModel)

class BaseController(Generic[T, U]):
    def __init__(self, router: APIRouter, prefix: str):
        self.router = router
        self.prefix = prefix
        self._setup_routes()
    
    def _setup_routes(self):
        @self.router.get(f"/{self.prefix}", response_model=List[T])
        async def get_all():
            return await self.get_all()
        
        @self.router.get(f"/{self.prefix}/{{id}}", response_model=T)
        async def get_by_id(id: str):
            return await self.get_by_id(id)
        
        @self.router.post(f"/{self.prefix}", response_model=T)
        async def create(item: U):
            return await self.create(item)
        
        @self.router.put(f"/{self.prefix}/{{id}}", response_model=T)
        async def update(id: str, item: U):
            return await self.update(id, item)
        
        @self.router.delete(f"/{self.prefix}/{{id}}")
        async def delete(id: str):
            return await self.delete(id)
    