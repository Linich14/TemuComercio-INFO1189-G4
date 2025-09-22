"""
Usuario entity - Domain layer
Represents a user in the system with authentication and role information.
"""
from datetime import datetime
from typing import Optional
from .base_entity import BaseEntity


class Usuario(BaseEntity):
    """
    Usuario entity following Domain-Driven Design principles.
    Represents a user with authentication credentials and role information.
    
    This entity focuses solely on data representation and basic business invariants.
    Complex business logic is delegated to domain services.
    """
    
    def __init__(
        self,
        usua_id: Optional[int] = None,
        usua_rut: str = "",
        usua_email: str = "",
        usua_pass: str = "",
        usua_creado: Optional[datetime] = None,
        usua_actualizado: Optional[datetime] = None,
        usua_estado: int = 1,  # Default: habilitado
        rous_id: int = 1  # Default role ID
    ):
        """
        Initialize Usuario entity.
        
        Args:
            usua_id: User ID (auto-generated if None)
            usua_rut: Chilean RUT identifier
            usua_email: User email address
            usua_pass: Hashed password
            usua_creado: Creation timestamp
            usua_actualizado: Last update timestamp
            usua_estado: User status (1=enabled, 0=disabled)
            rous_id: Role ID reference
        """
        super().__init__(usua_id)
        self.usua_id = usua_id  # Explicit assignment for compatibility
        self.usua_rut = usua_rut
        self.usua_email = usua_email
        self.usua_pass = usua_pass
        self.usua_creado = usua_creado or datetime.utcnow()
        self.usua_actualizado = usua_actualizado
        self.usua_estado = usua_estado
        self.rous_id = rous_id
    
    def __str__(self) -> str:
        return f"Usuario(id={self.usua_id}, email={self.usua_email}, rut={self.usua_rut})"
    
    def __repr__(self) -> str:
        return (f"Usuario(usua_id={self.usua_id}, usua_rut='{self.usua_rut}', "
                f"usua_email='{self.usua_email}', usua_estado={self.usua_estado})")