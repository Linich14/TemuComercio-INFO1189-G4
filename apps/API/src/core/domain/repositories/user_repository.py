from abc import ABC, abstractmethod
from typing import Optional
from ..entities.user import User

class UserRepositoryInterface(ABC):
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        pass
    
    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def exists_by_rut(self, rut: str) -> bool:
        pass
    
    @abstractmethod
    def update_last_login(self, user_id: int) -> None:
        pass