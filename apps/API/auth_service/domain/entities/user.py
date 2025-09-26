from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class User:
    """Entidad Usuario del dominio"""
    id: Optional[str]
    email: str
    password: str
    estado: bool
    id_role: Optional[int] = None
    rut: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def update_timestamp(self) -> None:
        """Actualiza el timestamp de modificación"""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> dict:
        """Convierte la entidad a diccionario"""
        return {
            'id': str(self.id) if self.id else None,
            'email': self.email,
            'password': self.password,
            'estado': self.estado,
            'rut': self.rut,
            'id_role': self.id_role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
