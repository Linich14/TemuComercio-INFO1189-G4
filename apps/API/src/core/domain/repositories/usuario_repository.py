"""
Usuario repository interface - Domain layer
Abstract repository interface for Usuario operations.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.usuario import Usuario


class UsuarioRepository(ABC):
    """
    Abstract repository interface for Usuario operations.
    Following Repository pattern and Dependency Inversion Principle.
    """
    
    @abstractmethod
    def create(self, usuario: Usuario) -> Usuario:
        """
        Create a new usuario.
        
        Args:
            usuario: Usuario entity to create
            
        Returns:
            Created Usuario entity with assigned ID
            
        Raises:
            RepositoryError: If creation fails
        """
        pass
    
    @abstractmethod
    def get_by_id(self, usua_id: int) -> Optional[Usuario]:
        """
        Get usuario by ID.
        
        Args:
            usua_id: Usuario ID
            
        Returns:
            Usuario entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_by_email(self, usua_email: str) -> Optional[Usuario]:
        """
        Get usuario by email.
        
        Args:
            usua_email: Usuario email
            
        Returns:
            Usuario entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_by_rut(self, usua_rut: str) -> Optional[Usuario]:
        """
        Get usuario by RUT.
        
        Args:
            usua_rut: Usuario RUT
            
        Returns:
            Usuario entity if found, None otherwise
        """
        pass
    
    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """
        Update an existing usuario.
        
        Args:
            usuario: Usuario entity with updated data
            
        Returns:
            Updated Usuario entity
            
        Raises:
            RepositoryError: If update fails
        """
        pass
    
    @abstractmethod
    def delete(self, usua_id: int) -> bool:
        """
        Delete usuario by ID.
        
        Args:
            usua_id: Usuario ID
            
        Returns:
            True if deleted successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def list_all(self, active_only: bool = True) -> List[Usuario]:
        """
        List all usuarios.
        
        Args:
            active_only: If True, return only enabled usuarios
            
        Returns:
            List of Usuario entities
        """
        pass
    
    @abstractmethod
    def list_by_role(self, rous_id: int, active_only: bool = True) -> List[Usuario]:
        """
        List usuarios by role.
        
        Args:
            rous_id: Role ID
            active_only: If True, return only enabled usuarios
            
        Returns:
            List of Usuario entities
        """
        pass
    
    @abstractmethod
    def exists_email(self, usua_email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if email already exists.
        
        Args:
            usua_email: Email to check
            exclude_id: Usuario ID to exclude from check (for updates)
            
        Returns:
            True if email exists, False otherwise
        """
        pass
    
    @abstractmethod
    def exists_rut(self, usua_rut: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if RUT already exists.
        
        Args:
            usua_rut: RUT to check
            exclude_id: Usuario ID to exclude from check (for updates)
            
        Returns:
            True if RUT exists, False otherwise
        """
        pass