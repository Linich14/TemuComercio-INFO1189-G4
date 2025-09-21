# core/application/use_cases/login_use_case.py
from ..dto.auth_dto import LoginRequestDTO, AuthResponseDTO
from ...domain.repositories.user_repository import UserRepositoryInterface
from ...domain.services.auth_service import AuthServiceInterface
from ...domain.services.password_service import PasswordServiceInterface

class LoginUseCase:
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
        # Buscar usuario por email
        user = self.user_repository.find_by_email(login_data.email)
        if not user:
            raise Exception("Email o contraseña incorrectos")
        
        # Verificar contraseña
        if not self.password_service.verify_password(login_data.password, user.password_hash):
            raise Exception("Email o contraseña incorrectos")
        
        # Verificar que la cuenta esté activa
        if not user.is_active:
            raise Exception("La cuenta está desactivada")
        
        # Verificar que el email esté verificado
        if not user.is_verified:
            raise Exception("Debes verificar tu email antes de iniciar sesión")
        
        # Actualizar último login
        self.user_repository.update_last_login(user.id)
        
        # Generar tokens
        auth_token = self.auth_service.generate_tokens(user)
        
        return AuthResponseDTO.from_user_and_tokens(user, auth_token)