"""
Dependency injection container for Clean Architecture.
Follows Dependency Inversion Principle.
"""
from typing import Dict, Any, Type
from abc import ABC, abstractmethod


class Container:
    """
    Simple dependency injection container.
    Manages dependencies and their lifecycles.
    """
    
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}
    
    def register(self, interface: Type, implementation: Type, singleton: bool = True):
        """Register a service implementation."""
        key = interface.__name__
        self._services[key] = {
            'implementation': implementation,
            'singleton': singleton
        }
    
    def get(self, interface: Type):
        """Get service instance."""
        key = interface.__name__
        
        if key not in self._services:
            raise ValueError(f"Service {key} not registered")
        
        service_config = self._services[key]
        
        if service_config['singleton']:
            if key not in self._singletons:
                self._singletons[key] = service_config['implementation']()
            return self._singletons[key]
        else:
            return service_config['implementation']()


# Global container instance
container = Container()


def configure_dependencies():
    """
    Configure all dependencies.
    This should be called during Django startup.
    """
    from ...core.domain.repositories.product_repository import ProductRepository
    from ...infrastructure.repositories.supabase_product_repository import SupabaseProductRepository
    
    # Register repositories (using Supabase-enhanced repository)
    container.register(ProductRepository, SupabaseProductRepository)


def get_container() -> Container:
    """Get the global container instance."""
    return container