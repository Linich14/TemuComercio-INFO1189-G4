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
    
    # Métodos específicos para obtener servicios registrados
    def get_user_repository(self):
        """Get user repository instance."""
        if 'user_repository' not in self._singletons:
            from ...infrastructure.repositories.django_user_repository import DjangoUserRepository
            self._singletons['user_repository'] = DjangoUserRepository()
        return self._singletons['user_repository']
    
    def get_auth_service(self):
        """Get authentication service instance."""
        if 'auth_service' not in self._singletons:
            from ...infrastructure.external_services.session_db_auth_service import SessionDBAuthService
            self._singletons['auth_service'] = SessionDBAuthService()
        return self._singletons['auth_service']
    
    def get_password_service(self):
        """Get password service instance."""
        if 'password_service' not in self._singletons:
            from ...infrastructure.external_services.password_services import DjangoPasswordService
            self._singletons['password_service'] = DjangoPasswordService()
        return self._singletons['password_service']
    
    def get_login_use_case(self):
        """Get login use case instance."""
        if 'login_use_case' not in self._singletons:
            from ...core.application.use_cases.login_use_case import LoginUseCase
            self._singletons['login_use_case'] = LoginUseCase(
                user_repository=self.get_user_repository(),
                auth_service=self.get_auth_service(),
                password_service=self.get_password_service()
            )
        return self._singletons['login_use_case']

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