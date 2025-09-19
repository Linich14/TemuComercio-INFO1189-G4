"""
Base repository interface following Interface Segregation Principle.
This interface defines the contract for all repositories.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Any

T = TypeVar('T')


class BaseRepository(ABC, Generic[T]):
    """
    Generic repository interface that follows SOLID principles.
    All repository implementations must implement these methods.
    """
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: Any) -> Optional[T]:
        """Get entity by its ID."""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[T]:
        """Get all entities."""
        pass
    
    @abstractmethod
    async def update(self, entity: T) -> T:
        """Update an existing entity."""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: Any) -> bool:
        """Delete an entity by its ID."""
        pass
    
    @abstractmethod
    async def exists(self, entity_id: Any) -> bool:
        """Check if entity exists."""
        pass