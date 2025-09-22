from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthToken:
    """Entidad para tokens de autenticación"""
    access_token: str
    refresh_token: str
    expires_at: int
    token_type: str = "Bearer"
    user_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convierte el token a diccionario"""
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'token_type': self.token_type,
            'user_id': self.user_id
        }
