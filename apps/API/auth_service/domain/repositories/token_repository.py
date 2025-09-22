from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

class TokenRepositoryInterface(ABC):
    """Interface para el repositorio de tokens"""
    
    @abstractmethod
    def save_refresh_token(self, user_id: str, token: str, expires_at: datetime) -> bool:
        """Guarda un refresh token"""
        pass
    
    @abstractmethod
    def get_refresh_token(self, token: str) -> Optional[dict]:
        """Obtiene información de un refresh token"""
        pass
    
    @abstractmethod
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoca un refresh token"""
        pass
    
    @abstractmethod
    def revoke_all_user_tokens(self, user_id: str) -> bool:
        """Revoca todos los tokens de un usuario"""
        pass
    
    @abstractmethod
    def clean_expired_tokens(self) -> int:
        """Limpia tokens expirados"""
        pass
