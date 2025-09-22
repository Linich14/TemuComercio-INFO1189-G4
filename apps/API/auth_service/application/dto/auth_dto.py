from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class LoginRequestDTO:
    """DTO para solicitud de login"""
    email: str
    password: str
    
    def __post_init__(self):
        if self.email:
            self.email = self.email.lower().strip()

@dataclass
class RegisterRequestDTO:
    """DTO para solicitud de registro"""
    email: str
    password: str
    first_name: str
    last_name: str
    rut: Optional[str] = None
    id_role: Optional[int] = None
    
    def __post_init__(self):
        if self.email:
            self.email = self.email.lower().strip()
        if self.first_name:
            self.first_name = self.first_name.strip().title()
        if self.last_name:
            self.last_name = self.last_name.strip().title()
        if self.rut:
            self.rut = self.rut.replace(".", "").replace("-", "").upper().strip()

@dataclass
class AuthResponseDTO:
    """DTO para respuesta de autenticación"""
    access_token: str
    refresh_token: str
    expires_at: int
    user: Dict[str, Any]
    token_type: str = "Bearer"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'expires_at': self.expires_at,
            'token_type': self.token_type,
            'user': self.user
        }

@dataclass
class RefreshTokenRequestDTO:
    """DTO para solicitud de refresh token"""
    refresh_token: str

@dataclass
class UserProfileDTO:
    """DTO para perfil de usuario"""
    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    rut: Optional[str] = None
    id_role: Optional[int] = None
    is_active: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'rut': self.rut,
            'id_role': self.id_role,
            'is_active': self.is_active
        }
