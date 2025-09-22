"""
Base entity class following Domain-Driven Design principles.
All domain entities should inherit from this base class.
"""
from abc import ABC
from datetime import datetime
from typing import Any


class BaseEntity(ABC):
    """
    Base class for all domain entities.
    Follows Single Responsibility Principle - handles common entity concerns.
    """
    
    def __init__(self, id: Any = None):
        self._id = id
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
    
    @property
    def id(self) -> Any:
        return self._id
    
    @property
    def created_at(self) -> datetime:
        return self._created_at
    
    @property
    def updated_at(self) -> datetime:
        return self._updated_at
    
    def update_timestamp(self) -> None:
        """Update the last modified timestamp."""
        self._updated_at = datetime.now()
    
    def __eq__(self, other) -> bool:
        """Entities are equal if they have the same ID and type."""
        if not isinstance(other, self.__class__):
            return False
        return self._id == other._id
    
    def __hash__(self) -> int:
        """Hash based on entity ID."""
        return hash(self._id)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id})"