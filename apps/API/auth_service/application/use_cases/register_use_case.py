from ..dto.auth_dto import UserCreateDTO, UserResponseDTO
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.services.password_service import PasswordServiceInterface
from ...domain.services.validation_service import ValidationServiceInterface
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
    
    def execute(self, user_dto: UserCreateDTO) -> UserResponseDTO:
        """Ejecutar caso de uso de registro"""
        # Validar datos de entrada
        self.validation_service.validate_email(user_dto.email)
        if user_dto.rut:
            self.validation_service.validate_rut(user_dto.rut)
        
        # Verificar que el usuario no existe
        existing_user = self.user_repository.find_by_email(user_dto.email)
        if existing_user:
            raise UserAlreadyExistsException("El usuario ya existe")
        
        # Hashear contraseña
        hashed_password = self.password_service.hash_password(user_dto.password)
        
        # Crear entidad de usuario
        user = User(
            id=None,
            email=user_dto.email,
            password=hashed_password,
            estado=user_dto.estado,
            rut=user_dto.rut,
            id_role=user_dto.id_role
        )
        
        # Guardar usuario
        created_user = self.user_repository.create(user)
        
        # Retornar DTO de respuesta
        return UserResponseDTO.from_user_entity(created_user)
