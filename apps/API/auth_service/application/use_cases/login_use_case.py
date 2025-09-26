from ..dto.auth_dto import LoginRequestDTO, AuthResponseDTO
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.services.auth_service import AuthServiceInterface
from ...domain.services.password_service import PasswordServiceInterface
from ...domain.exceptions.auth_exceptions import (
    InvalidCredentialsException, 
    UserNotFoundException,
    InactiveUserException
)

class LoginUseCase:
    """Caso de uso para login de usuario"""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        auth_service: AuthServiceInterface,
        password_service: PasswordServiceInterface
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service
        self.password_service = password_service
    
    def execute(self, login_data: LoginRequestDTO) -> AuthResponseDTO:
        """
        Ejecuta el proceso de login
        
        Args:
            login_data: Datos de login del usuario
            
        Returns:
            AuthResponseDTO: Respuesta con tokens y datos del usuario
            
        Raises:
            UserNotFoundException: Si el usuario no existe
            InvalidCredentialsException: Si las credenciales son incorrectas
            InactiveUserException: Si el usuario está inactivo
        """
        # Buscar usuario por email
        user = self.user_repository.get_by_email(login_data.email)
        if not user:
            raise UserNotFoundException("Usuario no encontrado")
        
        # Verificar que la cuenta esté activa
        if not user.estado:
            raise InactiveUserException("Cuenta desactivada")
        
        # Verificar contraseña
        if not self.password_service.verify_password(login_data.password, user.password):
            raise InvalidCredentialsException("Credenciales inválidas")
        
        # Generar tokens
        auth_token = self.auth_service.generate_tokens(user)
        
        # Preparar respuesta
        return AuthResponseDTO(
            access_token=auth_token.access_token,
            refresh_token=auth_token.refresh_token,
            expires_at=auth_token.expires_at,
            user=user.to_dict()
        )
