"""
Base DTO (Data Transfer Object) following Single Responsibility Principle.
DTOs are responsible only for data transport between layers.
"""
from abc import ABC
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class BaseDTO(ABC):
    """
    Base class for all Data Transfer Objects.
    Follows Single Responsibility - only for data transport.
    """
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert DTO to dictionary."""
        result = {}
        for field_name, field_value in self.__dict__.items():
            if isinstance(field_value, BaseDTO):
                result[field_name] = field_value.to_dict()
            elif isinstance(field_value, list):
                result[field_name] = [
                    item.to_dict() if isinstance(item, BaseDTO) else item
                    for item in field_value
                ]
            else:
                result[field_name] = field_value
        return result


@dataclass
class BaseResponseDTO(BaseDTO):
    """Base response DTO with common response fields."""
    success: bool = True
    message: str = ""


@dataclass
class BaseRequestDTO(BaseDTO):
    """Base request DTO for input validation."""
    pass


@dataclass
class PaginationDTO(BaseDTO):
    """DTO for pagination information."""
    page: int = 1
    page_size: int = 20
    total_pages: int = 0
    total_items: int = 0
    has_next: bool = False
    has_previous: bool = False