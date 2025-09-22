"""
Usuario use cases - Application layer
Business logic for Usuario operations.
"""
import hashlib
from typing import Optional
from datetime import datetime

from ..dto.usuario_dto import CreateUsuarioDTO, UpdateUsuarioDTO, UsuarioResponseDTO
from ...domain.entities.usuario import Usuario
from ...domain.repositories.usuario_repository import UsuarioRepository
from ...domain.services.validation_services import DomainEmailValidator, DomainRutValidator
from ...domain.services.user_state_service import DomainUserStateManager


class CreateUsuarioUseCase:
    """
    Use case for creating a new Usuario.
    Follows Single Responsibility Principle.
    """
    
    def __init__(
        self, 
        usuario_repository: UsuarioRepository,
        email_validator: DomainEmailValidator = None,
        rut_validator: DomainRutValidator = None
    ):
        self.usuario_repository = usuario_repository
        self.email_validator = email_validator or DomainEmailValidator()
        self.rut_validator = rut_validator or DomainRutValidator()
    
    def execute(self, dto: CreateUsuarioDTO) -> UsuarioResponseDTO:
        """
        Create a new usuario with validation.
        
        Args:
            dto: Data for creating the usuario
            
        Returns:
            UsuarioResponseDTO with created usuario data
            
        Raises:
            ValueError: If validation fails
            RepositoryError: If creation fails
        """
        # Validate email format
        if not self.email_validator.validate(dto.usua_email):
            raise ValueError("Invalid email format")
        
        # Validate RUT format
        if not self.rut_validator.validate(dto.usua_rut):
            raise ValueError("Invalid RUT format")
        
        # Validate email uniqueness
        if self.usuario_repository.exists_email(dto.usua_email):
            raise ValueError(f"Email {dto.usua_email} already exists")
        
        # Validate RUT uniqueness
        if self.usuario_repository.exists_rut(dto.usua_rut):
            raise ValueError(f"RUT {dto.usua_rut} already exists")
        
        # Create Usuario entity
        usuario = Usuario(
            usua_rut=dto.usua_rut,
            usua_email=dto.usua_email,
            usua_pass=self._hash_password(dto.usua_pass),
            usua_estado=dto.usua_estado,
            rous_id=dto.rous_id
        )
        
        # Create usuario
        created_usuario = self.usuario_repository.create(usuario)
        
        # Return response DTO
        return UsuarioResponseDTO.from_entity(created_usuario)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()


class GetUsuarioUseCase:
    """Use case for getting a Usuario by ID."""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
    
    def execute(self, usua_id: int) -> Optional[UsuarioResponseDTO]:
        """Get usuario by ID."""
        usuario = self.usuario_repository.get_by_id(usua_id)
        
        if usuario:
            return UsuarioResponseDTO.from_entity(usuario)
        
        return None


class UpdateUsuarioUseCase:
    """Use case for updating a Usuario."""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
    
    def execute(self, dto: UpdateUsuarioDTO) -> UsuarioResponseDTO:
        """
        Update an existing usuario.
        
        Args:
            dto: Data for updating the usuario
            
        Returns:
            UsuarioResponseDTO with updated usuario data
            
        Raises:
            ValueError: If validation fails or usuario not found
            RepositoryError: If update fails
        """
        # Get existing usuario
        existing_usuario = self.usuario_repository.get_by_id(dto.usua_id)
        if not existing_usuario:
            raise ValueError(f"Usuario with ID {dto.usua_id} not found")
        
        # Validate email uniqueness if changed
        if dto.usua_email and dto.usua_email != existing_usuario.usua_email:
            if self.usuario_repository.exists_email(dto.usua_email, dto.usua_id):
                raise ValueError(f"Email {dto.usua_email} already exists")
        
        # Validate RUT uniqueness if changed
        if dto.usua_rut and dto.usua_rut != existing_usuario.usua_rut:
            if self.usuario_repository.exists_rut(dto.usua_rut, dto.usua_id):
                raise ValueError(f"RUT {dto.usua_rut} already exists")
        
        # Update entity fields
        if dto.usua_rut:
            existing_usuario.usua_rut = dto.usua_rut
        if dto.usua_email:
            existing_usuario.usua_email = dto.usua_email
        if dto.usua_pass:
            existing_usuario.usua_pass = self._hash_password(dto.usua_pass)
        if dto.rous_id is not None:
            existing_usuario.rous_id = dto.rous_id
        if dto.usua_estado is not None:
            existing_usuario.usua_estado = dto.usua_estado
        
        # Update timestamp
        existing_usuario.update_last_modified()
        
        # Validate entity
        if not existing_usuario.validate_email():
            raise ValueError("Invalid email format")
        
        if not existing_usuario.validate_rut():
            raise ValueError("Invalid RUT format")
        
        # Update usuario
        updated_usuario = self.usuario_repository.update(existing_usuario)
        
        # Return response DTO
        return UsuarioResponseDTO.from_entity(updated_usuario)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()


class ListUsuariosUseCase:
    """Use case for listing usuarios."""
    
    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository
    
    def execute(self, active_only: bool = True) -> list[UsuarioResponseDTO]:
        """List all usuarios."""
        usuarios = self.usuario_repository.list_all(active_only)
        return [UsuarioResponseDTO.from_entity(usuario) for usuario in usuarios]


class DisableUsuarioUseCase:
    """Use case for disabling a Usuario."""
    
    def __init__(
        self, 
        usuario_repository: UsuarioRepository,
        user_state_manager: DomainUserStateManager = None
    ):
        self.usuario_repository = usuario_repository
        self.user_state_manager = user_state_manager or DomainUserStateManager()
    
    def execute(self, usua_id: int) -> UsuarioResponseDTO:
        """
        Disable a usuario.
        
        Args:
            usua_id: Usuario ID to disable
            
        Returns:
            UsuarioResponseDTO with updated usuario data
            
        Raises:
            ValueError: If usuario not found
        """
        usuario = self.usuario_repository.get_by_id(usua_id)
        if not usuario:
            raise ValueError(f"Usuario with ID {usua_id} not found")
        
        self.user_state_manager.disable_user(usuario)
        updated_usuario = self.usuario_repository.update(usuario)
        
        return UsuarioResponseDTO.from_entity(updated_usuario)


class EnableUsuarioUseCase:
    """Use case for enabling a Usuario."""
    
    def __init__(
        self, 
        usuario_repository: UsuarioRepository,
        user_state_manager: DomainUserStateManager = None
    ):
        self.usuario_repository = usuario_repository
        self.user_state_manager = user_state_manager or DomainUserStateManager()
    
    def execute(self, usua_id: int) -> UsuarioResponseDTO:
        """
        Enable a usuario.
        
        Args:
            usua_id: Usuario ID to enable
            
        Returns:
            UsuarioResponseDTO with updated usuario data
            
        Raises:
            ValueError: If usuario not found
        """
        usuario = self.usuario_repository.get_by_id(usua_id)
        if not usuario:
            raise ValueError(f"Usuario with ID {usua_id} not found")
        
        self.user_state_manager.enable_user(usuario)
        updated_usuario = self.usuario_repository.update(usuario)
        
        return UsuarioResponseDTO.from_entity(updated_usuario)