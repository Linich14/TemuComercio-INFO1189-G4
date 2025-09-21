"""
Infrastructure dependency provider implementation.
This module implements the dependency provider for infrastructure layer.
"""
from ..repositories.django_usuario_repository import DjangoUsuarioRepository
from ...core.domain.repositories.usuario_repository import UsuarioRepository
from ...interfaces.api.dependencies import DependencyProvider


class InfrastructureDependencyProvider:
    """Concrete implementation of dependency provider for infrastructure layer."""
    
    def get_usuario_repository(self) -> UsuarioRepository:
        """Get Django-based usuario repository implementation."""
        return DjangoUsuarioRepository()