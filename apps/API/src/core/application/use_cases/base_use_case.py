"""
Base use case interface following Single Responsibility Principle.
Each use case should have a single, well-defined responsibility.
"""
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any

Request = TypeVar('Request')
Response = TypeVar('Response')


class BaseUseCase(ABC, Generic[Request, Response]):
    """
    Base class for all use cases in the application layer.
    Follows Command pattern and Single Responsibility Principle.
    """
    
    @abstractmethod
    async def execute(self, request: Request) -> Response:
        """
        Execute the use case with the given request.
        
        Args:
            request: The input data for the use case
            
        Returns:
            The response from executing the use case
        """
        pass


class BaseQuery(ABC, Generic[Request, Response]):
    """
    Base class for query operations (CQRS pattern).
    Separates read operations from commands.
    """
    
    @abstractmethod
    async def execute(self, request: Request) -> Response:
        """Execute the query with the given request."""
        pass


class BaseCommand(ABC, Generic[Request, Response]):
    """
    Base class for command operations (CQRS pattern).
    Separates write operations from queries.
    """
    
    @abstractmethod
    async def execute(self, request: Request) -> Response:
        """Execute the command with the given request."""
        pass