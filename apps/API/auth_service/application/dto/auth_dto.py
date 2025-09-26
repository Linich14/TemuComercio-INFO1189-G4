from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

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
    rut: Optional[str] = None
    id_role: Optional[int] = None
    estado: bool = True
    
    def __post_init__(self):
        if self.email:
            self.email = self.email.lower().strip()
        if self.rut:
            self.rut = self.rut.replace(".", "").replace("-", "").upper().strip()
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'email': self.email,
            'password': self.password,
            'rut': self.rut,
            'id_role': self.id_role,
            'estado': self.estado
        }

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
    rut: Optional[str] = None
    id_role: Optional[int] = None
    estado: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'rut': self.rut,
            'id_role': self.id_role,
            'estado': self.estado,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

@dataclass
class UserCreateDTO:
    """DTO para crear usuarios"""
    email: str
    password: str
    rut: Optional[str] = None
    id_role: Optional[int] = None
    estado: bool = True

@dataclass
class UserResponseDTO:
    """DTO para respuestas de usuario"""
    id: str
    email: str
    estado: bool
    rut: Optional[str] = None
    id_role: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_user_entity(cls, user):
        """Crear DTO desde entidad de usuario"""
        return cls(
            id=str(user.id),
            email=user.email,
            estado=user.estado,
            rut=user.rut,
            id_role=user.id_role,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'estado': self.estado,
            'rut': self.rut,
            'id_role': self.id_role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

@dataclass
class LoginDTO:
    """DTO para login"""
    email: str
    password: str

@dataclass
class LoginResponseDTO:
    """DTO para respuesta de login"""
    access_token: str
    refresh_token: str
    user: UserResponseDTO
    expires_at: int

@dataclass
class RefreshTokenDTO:
    """DTO para refresh token"""
    refresh_token: str

@dataclass
class RefreshTokenResponseDTO:
    """DTO para respuesta de refresh token"""
    access_token: str
    expires_in: int
