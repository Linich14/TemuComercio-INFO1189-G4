from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.user import User

class UserRepositoryInterface(ABC):
    """Interface para el repositorio de usuarios"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Crea un nuevo usuario"""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario existente"""
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """Elimina un usuario"""
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """Verifica si existe un usuario con el email dado"""
        pass
    
    @abstractmethod
    def exists_by_rut(self, rut: str) -> bool:
        """Verifica si existe un usuario con el RUT dado"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """Obtiene un usuario por ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        pass
    
    @abstractmethod
    def get_by_rut(self, rut: str) -> Optional[User]:
        """Obtiene un usuario por RUT"""
        pass
    
    @abstractmethod
    def list_all(self, active_only: bool = True) -> List[User]:
        """Lista todos los usuarios"""
        pass
    
    @abstractmethod
    def count_users(self, active_only: bool = True) -> int:
        """Cuenta el número de usuarios"""
        pass
