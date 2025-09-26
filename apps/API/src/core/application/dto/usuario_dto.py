"""
Usuario DTOs - Application layer
Data Transfer Objects for Usuario operations.
"""
from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class CreateUsuarioDTO:
    """DTO for creating a new Usuario."""
    usua_rut: str
    usua_email: str
    usua_pass: str  # Plain password (will be hashed)
    rous_id: int = 4  # Default to "Usuario" role
    usua_estado: int = 1  # Default: habilitado


@dataclass
class UpdateUsuarioDTO:
    """DTO for updating an existing Usuario."""
    usua_id: int
    usua_rut: Optional[str] = None
    usua_email: Optional[str] = None
    usua_pass: Optional[str] = None  # Plain password (will be hashed)
    rous_id: Optional[int] = None
    usua_estado: Optional[int] = None


@dataclass
class UsuarioResponseDTO:
    """DTO for Usuario response (without sensitive data)."""
    usua_id: int
    usua_rut: str
    usua_email: str
    usua_creado: datetime
    usua_actualizado: Optional[datetime]
    usua_estado: int
    rous_id: int
    rol_nombre: Optional[str] = None  # Include role name for convenience
    
    @classmethod
    def from_entity(cls, usuario, rol_nombre: Optional[str] = None):
        """Create DTO from Usuario entity."""
        return cls(
            usua_id=usuario.usua_id,
            usua_rut=usuario.usua_rut,
            usua_email=usuario.usua_email,
            usua_creado=usuario.usua_creado,
            usua_actualizado=usuario.usua_actualizado,
            usua_estado=usuario.usua_estado,
            rous_id=usuario.rous_id,
            rol_nombre=rol_nombre
        )


@dataclass
class UsuarioListDTO:
    """DTO for Usuario list response."""
    usuarios: list[UsuarioResponseDTO]
    total: int
    page: int
    page_size: int


@dataclass
class LoginRequestDTO:
    """DTO for login request."""
    usua_email: str
    usua_pass: str


@dataclass
class LoginResponseDTO:
    """DTO for login response."""
    token: str
    usuario: UsuarioResponseDTO
    expires_at: datetime