from abc import ABC, abstractmethod

class PasswordServiceInterface(ABC):
    """Interface para el servicio de manejo de contraseñas"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña"""
        pass

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        pass
    
    @abstractmethod
    def generate_password(self, length: int = 12) -> str:
        """Genera una contraseña aleatoria"""
        pass
    
    @abstractmethod
    def is_password_strong(self, password: str) -> bool:
        """Verifica si una contraseña es fuerte"""
        pass
