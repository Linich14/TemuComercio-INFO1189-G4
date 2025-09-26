"""
Configuration module for dependency injection in interfaces layer.
This module provides a way to inject dependencies without violating Clean Architecture.
"""
from typing import Protocol
from ...core.domain.repositories.usuario_repository import UsuarioRepository


class DependencyProvider(Protocol):
    """Protocol for dependency providers."""
    
    def get_usuario_repository(self) -> UsuarioRepository:
        """Get usuario repository instance."""
        ...


class _DependencyRegistry:
    """Registry for dependency providers."""
    
    def __init__(self):
        self._provider: DependencyProvider = None
    
    def register_provider(self, provider: DependencyProvider) -> None:
        """Register a dependency provider."""
        self._provider = provider
    
    def get_usuario_repository(self) -> UsuarioRepository:
        """Get usuario repository from registered provider."""
        if not self._provider:
            raise RuntimeError("No dependency provider registered")
        return self._provider.get_usuario_repository()


# Global dependency registry
dependency_registry = _DependencyRegistry()


def get_usuario_repository() -> UsuarioRepository:
    """Get usuario repository instance."""
    return dependency_registry.get_usuario_repository()