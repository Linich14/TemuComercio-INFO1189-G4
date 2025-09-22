from ..dto.auth_dto import RegisterRequestDTO, UserProfileDTO
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.services.password_service import PasswordServiceInterface
from ...domain.services.validation_service import ValidationServiceInterface
from ...domain.entities.user import User
from ...domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    ValidationException
)

class RegisterUseCase:
    """Caso de uso para registro de usuario"""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        password_service: PasswordServiceInterface,
        validation_service: ValidationServiceInterface
    ):
        self.user_repository = user_repository
        self.password_service = password_service
        self.validation_service = validation_service
    
    def execute(self, register_data: RegisterRequestDTO) -> UserProfileDTO:
        """
        Ejecuta el proceso de registro
        
        Args:
            register_data: Datos de registro del usuario
            
        Returns:
            UserProfileDTO: Datos del usuario registrado
            
        Raises:
            UserAlreadyExistsException: Si el usuario ya existe
            ValidationException: Si los datos no son válidos
        """
        # Validar datos de entrada
        self._validate_registration_data(register_data)
        
        # Verificar si el usuario ya existe
        if self.user_repository.exists_by_email(register_data.email):
            raise UserAlreadyExistsException("El email ya está registrado")
        
        if register_data.rut and self.user_repository.exists_by_rut(register_data.rut):
            raise UserAlreadyExistsException("El RUT ya está registrado")
        
        # Crear nuevo usuario
        hashed_password = self.password_service.hash_password(register_data.password)
        
        user = User(
            id=None,
            email=register_data.email,
            password=hashed_password,
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            rut=register_data.rut,
            id_role=register_data.id_role or 4,  # Default role
            is_active=True
        )
        
        # Guardar usuario
        created_user = self.user_repository.create(user)
        
        # Retornar perfil del usuario creado
        return UserProfileDTO(
            id=str(created_user.id),
            email=created_user.email,
            first_name=created_user.first_name,
            last_name=created_user.last_name,
            full_name=created_user.full_name,
            rut=created_user.rut,
            id_role=created_user.id_role,
            is_active=created_user.is_active
        )
    
    def _validate_registration_data(self, register_data: RegisterRequestDTO) -> None:
        """Valida los datos de registro"""
        errors = []
        
        # Validar email
        if not self.validation_service.validate_email(register_data.email):
            errors.append("Email inválido")
        
        # Validar contraseña
        password_validation = self.validation_service.validate_password(register_data.password)
        if not password_validation['is_valid']:
            errors.extend(password_validation['errors'])
        
        # Validar RUT si se proporciona
        if register_data.rut and not self.validation_service.validate_rut(register_data.rut):
            errors.append("RUT inválido")
        
        # Validar nombres
        if not register_data.first_name or not register_data.first_name.strip():
            errors.append("Nombre es requerido")
        
        if not register_data.last_name or not register_data.last_name.strip():
            errors.append("Apellido es requerido")
        
        if errors:
            raise ValidationException("; ".join(errors))
