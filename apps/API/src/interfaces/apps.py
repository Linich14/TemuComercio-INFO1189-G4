"""
Django application configuration for dependency injection setup.
This module configures Clean Architecture dependency injection at startup.
"""
from django.apps import AppConfig


class InterfacesConfig(AppConfig):
    """Configuration for interfaces app."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.interfaces'
    
    def ready(self):
        """Initialize dependency injection when Django starts."""
        from .api.dependencies import dependency_registry
        from ..infrastructure.providers.dependency_provider import InfrastructureDependencyProvider
        
        # Register infrastructure provider
        provider = InfrastructureDependencyProvider()
        dependency_registry.register_provider(provider)