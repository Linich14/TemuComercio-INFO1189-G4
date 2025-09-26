from dataclasses import dataclass
from typing import Optional

@dataclass
class AuthToken:
    """Entidad para tokens de autenticación"""
    id: str
    valor: str
    creado_en: int
    expira_en: Optional[int] = None
    activo: bool = True
    user_id: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convierte el token a diccionario"""
        return {
            'id': self.id,
            'valor': self.valor,
            'creado_en': self.creado_en,
            'expira_en': self.expira_en,
            'activo': self.activo,
            'user_id': self.user_id
        }
