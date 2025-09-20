"""
Domain service interface following Interface Segregation Principle.
Domain services contain business logic that doesn't naturally fit in entities.
"""
from abc import ABC, abstractmethod


class BaseDomainService(ABC):
    """
    Base interface for domain services.
    Domain services contain business logic that spans multiple entities
    or doesn't naturally belong to a single entity.
    """
    pass


class ValidationService(ABC):
    """
    Interface for validation services.
    Follows Single Responsibility - only handles validation logic.
    """
    
    @abstractmethod
    async def validate(self, entity) -> bool:
        """Validate an entity according to business rules."""
        pass
    
    @abstractmethod
    async def get_validation_errors(self, entity) -> list:
        """Get list of validation errors for an entity."""
        pass


class NotificationService(ABC):
    """
    Interface for notification services.
    Follows Interface Segregation - specific to notification concerns.
    """
    
    @abstractmethod
    async def send_notification(self, recipient: str, message: str) -> bool:
        """Send a notification to a recipient."""
        pass


class EventPublisher(ABC):
    """
    Interface for event publishing (Domain Events pattern).
    Follows Open/Closed principle - extensible for new event types.
    """
    
    @abstractmethod
    async def publish(self, event) -> None:
        """Publish a domain event."""
        pass