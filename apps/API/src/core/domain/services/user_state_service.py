"""
Usuario state management service.
Domain layer - Business logic for user state management.
"""
from datetime import datetime
from typing import Protocol


class UserStateManager(Protocol):
    """Protocol for user state management."""
    
    def enable_user(self, user) -> None:
        """Enable a user."""
        ...
    
    def disable_user(self, user) -> None:
        """Disable a user."""
        ...
    
    def is_enabled(self, user) -> bool:
        """Check if user is enabled."""
        ...


class DomainUserStateManager:
    """Domain implementation of user state management."""
    
    def enable_user(self, user) -> None:
        """
        Enable a user and update timestamp.
        
        Args:
            user: Usuario entity to enable
        """
        user.usua_estado = 1
        user.usua_actualizado = datetime.utcnow()
    
    def disable_user(self, user) -> None:
        """
        Disable a user and update timestamp.
        
        Args:
            user: Usuario entity to disable
        """
        user.usua_estado = 0
        user.usua_actualizado = datetime.utcnow()
    
    def is_enabled(self, user) -> bool:
        """
        Check if user is enabled.
        
        Args:
            user: Usuario entity to check
            
        Returns:
            True if user is enabled
        """
        return user.usua_estado == 1
    
    def update_last_modified(self, user) -> None:
        """
        Update the last modified timestamp.
        
        Args:
            user: Usuario entity to update
        """
        user.usua_actualizado = datetime.utcnow()