from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """Entidad Usuario del dominio"""
    id: Optional[str]
    email: str
    password: str
    first_name: str
    last_name: str
    is_active: bool
    rut: Optional[str] = None
    id_role: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def full_name(self) -> str:
        """Retorna el nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def update_timestamp(self) -> None:
        """Actualiza el timestamp de modificación"""
        self.updated_at = datetime.now()
    
    def is_valid_for_login(self) -> bool:
        """Verifica si el usuario puede hacer login"""
        return self.is_active and self.email and self.password
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': str(self.id) if self.id else None,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'rut': self.rut,
            'id_role': self.id_role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
