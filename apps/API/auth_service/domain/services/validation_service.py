from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ValidationServiceInterface(ABC):
    """Interface para el servicio de validación"""
    
    @abstractmethod
    def validate_email(self, email: str) -> bool:
        """Valida formato de email"""
        pass
    
    @abstractmethod
    def validate_rut(self, rut: str) -> bool:
        """Valida formato y dígito verificador de RUT chileno"""
        pass
    
    @abstractmethod
    def validate_password(self, password: str) -> Dict[str, Any]:
        """Valida una contraseña y retorna detalles de validación"""
        pass
    
    @abstractmethod
    def validate_user_data(self, user_data: Dict[str, Any]) -> List[str]:
        """Valida datos completos de usuario"""
        pass
