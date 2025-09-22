"""
RolUsuario entity - Domain layer
Represents user roles in the system.
"""
from typing import Optional
from .base_entity import BaseEntity


class RolUsuario(BaseEntity):
    """
    RolUsuario entity following Domain-Driven Design principles.
    Represents a user role with permissions and description.
    """
    
    def __init__(
        self,
        rous_id: Optional[int] = None,
        rous_nombre: str = "",
        rous_descripcion: str = "",
        rous_estado: int = 1  # Default: habilitado
    ):
        """
        Initialize RolUsuario entity.
        
        Args:
            rous_id: Role ID
            rous_nombre: Role name
            rous_descripcion: Role description
            rous_estado: Role status (1=enabled, 0=disabled)
        """
        super().__init__(rous_id)
        self.rous_nombre = rous_nombre
        self.rous_descripcion = rous_descripcion
        self.rous_estado = rous_estado
    
    def is_enabled(self) -> bool:
        """Check if role is enabled."""
        return self.rous_estado == 1
    
    def enable(self) -> None:
        """Enable the role."""
        self.rous_estado = 1
    
    def disable(self) -> None:
        """Disable the role."""
        self.rous_estado = 0
    
    def __str__(self) -> str:
        return f"RolUsuario(id={self.rous_id}, nombre={self.rous_nombre})"
    
    def __repr__(self) -> str:
        return (f"RolUsuario(rous_id={self.rous_id}, rous_nombre='{self.rous_nombre}', "
                f"rous_descripcion='{self.rous_descripcion}', rous_estado={self.rous_estado})")