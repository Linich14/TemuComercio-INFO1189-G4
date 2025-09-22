from abc import ABC, abstractmethod
from typing import Any, Dict
from ..entities.auth_token import AuthToken
from ..entities.user import User

class AuthServiceInterface(ABC):
    """Interface para el servicio de autenticación"""
    
    @abstractmethod
    def generate_tokens(self, user: User) -> AuthToken:
        """Genera tokens de acceso y refresco para un usuario"""
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> Dict[str, Any]:
        """Verifica y decodifica un token de acceso"""
        pass
    
    @abstractmethod
    def refresh_access_token(self, refresh_token: str) -> AuthToken:
        """Renueva un token de acceso usando un refresh token"""
        pass
    
    @abstractmethod
    def revoke_token(self, token: str) -> bool:
        """Revoca un token"""
        pass
